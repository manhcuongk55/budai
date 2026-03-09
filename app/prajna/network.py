"""
Prajna Network 🪷 — Orchestrator cho 4 bộ lọc Bát Nhã.
Chạy 4 classifiers song song, tổng hợp scores, quyết định PASS / REWRITE / REJECT.
"""

import asyncio
import logging
from typing import Callable, Optional

from app.prajna.config import PrajnaConfig, prajna_config
from app.prajna.models import PrajnaAction, PrajnaAudit, PrajnaResult, PrajnaScore
from app.prajna.classifiers import (
    TruthClassifier,
    CompassionClassifier,
    EmptinessClassifier,
    HarmClassifier,
)

logger = logging.getLogger("budai.prajna")


class PrajnaNetwork:
    """
    Prajna Deep Learning Network 🪷
    Hệ Điều Hành Bát Nhã cho AI — đảm bảo mọi output tuân thủ 4 nguyên tắc.

    Pipeline:
        AI Response → [Truth, Compassion, Emptiness, Harm] → Decision → Output
    """

    def __init__(self, config: Optional[PrajnaConfig] = None):
        self.config = config or prajna_config
        self.truth = TruthClassifier()
        self.compassion = CompassionClassifier()
        self.emptiness = EmptinessClassifier()
        self.harm = HarmClassifier()

    async def filter(
        self,
        question: str,
        answer: str,
        context: str = "",
        generate_fn: Callable = None,
        rewrite_fn: Callable = None,
    ) -> PrajnaResult:
        """
        Filter an AI response through the Prajna Network.

        Args:
            question: Original user question
            answer: AI-generated answer to evaluate
            context: RAG context (if any)
            generate_fn: Async fn to call LLM for judging (from CostRouter)
            rewrite_fn: Async fn to call LLM for rewriting (from CostRouter)

        Returns:
            PrajnaResult with final_answer, scores, action, and audit_log
        """
        if not self.config.enabled:
            return PrajnaResult(
                action=PrajnaAction.PASS,
                original_answer=answer,
                final_answer=answer,
                total_attempts=0,
                scores=[],
                audit_log=[],
                prajna_passed=True,
            )

        original_answer = answer
        audit_log = []
        current_answer = answer

        for attempt in range(1, self.config.max_rewrite_attempts + 2):  # +1 for original + rewrites
            # Run all 4 classifiers in parallel
            scores = await self._evaluate_all(question, current_answer, context, generate_fn)

            # Determine action
            action = self._decide(scores)

            # Create audit entry
            audit = PrajnaAudit(
                attempt=attempt,
                scores=scores,
                action=action,
            )
            audit_log.append(audit)

            logger.info(
                f"🪷 Prajna attempt {attempt}: "
                f"T={self._get_score(scores, 'truth'):.2f} "
                f"C={self._get_score(scores, 'compassion'):.2f} "
                f"E={self._get_score(scores, 'emptiness'):.2f} "
                f"H={self._get_score(scores, 'harm'):.2f} "
                f"→ {action.value.upper()}"
            )

            if action == PrajnaAction.PASS:
                return PrajnaResult(
                    action=PrajnaAction.PASS,
                    original_answer=original_answer,
                    final_answer=current_answer,
                    total_attempts=attempt,
                    scores=scores,
                    audit_log=audit_log,
                    prajna_passed=True,
                )

            if action == PrajnaAction.REJECT:
                reject_answer = self._get_rejection_message(question, scores)
                return PrajnaResult(
                    action=PrajnaAction.REJECT,
                    original_answer=original_answer,
                    final_answer=reject_answer,
                    total_attempts=attempt,
                    scores=scores,
                    audit_log=audit_log,
                    prajna_passed=False,
                )

            # REWRITE: try to improve
            if attempt <= self.config.max_rewrite_attempts and rewrite_fn:
                feedback = self._build_rewrite_feedback(scores)
                audit.rewrite_prompt = feedback
                current_answer = await self._rewrite(
                    question, current_answer, context, feedback, rewrite_fn
                )
            else:
                # Max rewrites reached — accept with warning
                return PrajnaResult(
                    action=PrajnaAction.REWRITE,
                    original_answer=original_answer,
                    final_answer=current_answer,
                    total_attempts=attempt,
                    scores=scores,
                    audit_log=audit_log,
                    prajna_passed=False,
                )

        # Should not reach here, but safety return
        return PrajnaResult(
            action=PrajnaAction.REWRITE,
            original_answer=original_answer,
            final_answer=current_answer,
            total_attempts=self.config.max_rewrite_attempts + 1,
            scores=scores,
            audit_log=audit_log,
            prajna_passed=False,
        )

    async def _evaluate_all(
        self,
        question: str,
        answer: str,
        context: str,
        generate_fn: Callable,
    ) -> list[PrajnaScore]:
        """Run all 4 classifiers in parallel."""
        tasks = [
            self.truth.evaluate(question, answer, context, generate_fn,
                                self.config.truth_threshold),
            self.compassion.evaluate(question, answer, context, generate_fn,
                                    self.config.compassion_threshold),
            self.emptiness.evaluate(question, answer, context, generate_fn,
                                   self.config.emptiness_threshold),
            self.harm.evaluate(question, answer, context, generate_fn,
                              self.config.harm_threshold),
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        scores = []
        for r in results:
            if isinstance(r, Exception):
                logger.error(f"🪷 Classifier error: {r}")
                # Default to cautious pass on error
                scores.append(PrajnaScore(
                    classifier="error",
                    score=0.7,
                    passed=True,
                    feedback=f"Classifier error: {str(r)[:100]}",
                    threshold=0.5,
                ))
            else:
                scores.append(r)
        return scores

    def _decide(self, scores: list[PrajnaScore]) -> PrajnaAction:
        """Decide action based on all scores."""
        # Check harm first — if harmful, reject immediately
        harm_score = next((s for s in scores if s.classifier == "harm"), None)
        if harm_score and not harm_score.passed:
            return PrajnaAction.REJECT

        # Check if all others pass
        all_pass = all(s.passed for s in scores)
        if all_pass:
            return PrajnaAction.PASS

        # Some failed but not harmful → rewrite
        return PrajnaAction.REWRITE

    def _get_score(self, scores: list[PrajnaScore], name: str) -> float:
        """Get score value by classifier name."""
        for s in scores:
            if s.classifier == name:
                return s.score
        return 0.0

    def _build_rewrite_feedback(self, scores: list[PrajnaScore]) -> str:
        """Build feedback prompt from failed classifiers."""
        failed = [s for s in scores if not s.passed]
        feedback_parts = []
        for s in failed:
            feedback_parts.append(
                f"[{s.classifier.upper()}] (score: {s.score:.2f}, need: {s.threshold:.2f})\n"
                f"  Feedback: {s.feedback}"
            )
        return "\n\n".join(feedback_parts)

    async def _rewrite(
        self,
        question: str,
        answer: str,
        context: str,
        feedback: str,
        rewrite_fn: Callable,
    ) -> str:
        """Rewrite the answer incorporating Prajna feedback."""
        rewrite_prompt = f"""The following AI answer needs improvement based on Prajna (Bát Nhã) principles.

Original question: {question}

Current answer that needs improvement:
{answer}

Issues found by Prajna filters:
{feedback}

Please rewrite the answer to address these issues while keeping the factual content.
Rules:
- Maintain accuracy (Truth)
- Be compassionate and supportive (Compassion)
- Present multiple perspectives where appropriate (Emptiness)
- Ensure no harm (Non-Harm)

Rewrite the answer now:"""

        system_prompt = (
            "You are budAI 🪷 — rewriting an answer to align with Bát Nhã principles. "
            "Output ONLY the improved answer, no meta-commentary."
        )

        try:
            result = await rewrite_fn(
                prompt=rewrite_prompt,
                system_prompt=system_prompt,
                max_tokens=2048,
                temperature=0.3,
            )
            return result.text
        except Exception as e:
            logger.error(f"🪷 Rewrite failed: {e}. Keeping original answer.")
            return answer

    def _get_rejection_message(self, question: str, scores: list[PrajnaScore]) -> str:
        """Generate a compassionate rejection message."""
        harm_score = next((s for s in scores if s.classifier == "harm"), None)
        harm_feedback = harm_score.feedback if harm_score else ""

        return (
            "🪷 budAI từ chối trả lời câu hỏi này.\n\n"
            "Theo nguyên tắc Bát Nhã (Non-Harm / Không Gây Hại), "
            "câu trả lời có thể gây hại cho bạn hoặc người khác.\n\n"
            f"Lý do: {harm_feedback}\n\n"
            "Bố Đại nói: \"Mở túi vải ra, chỉ có những điều tốt lành thôi.\" 🪷\n\n"
            "Nếu bạn cần hỗ trợ, hãy đặt câu hỏi theo hướng tích cực hơn."
        )


# Singleton
prajna_network = PrajnaNetwork()
