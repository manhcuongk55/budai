"""
budAI MCP Server — Expose budAI capabilities as MCP tools for GoClaw.
GoClaw agents can call budAI Prajna filters, RAG queries, and cost routing
through the MCP (Model Context Protocol) bridge.
"""

import json
import logging
from typing import Any, Dict, List, Optional

from app.basao.protocol import (
    IntentEnvelope, BasaoResponse, AgentCapability, IntentType, TrustLevel,
)
from app.basao.firewall import basao_firewall
from app.prajna import prajna_network

logger = logging.getLogger("budai.basao.mcp")


# ─── budAI Agent Capability Declaration ──────────────────────────────

BUDAI_CAPABILITY = AgentCapability(
    agent_id="budai-prajna",
    agent_name="budAI 布袋 — Prajna AI OS",
    capabilities=[
        IntentType.FACT_CHECK.value,
        IntentType.KNOWLEDGE_QUERY.value,
        IntentType.DHARMA_QUERY.value,
        IntentType.PRAJNA_FILTER.value,
        IntentType.TRUTH_EVAL.value,
        IntentType.COMPASSION_EVAL.value,
        IntentType.HARM_DETECT.value,
        IntentType.ROUTE_TO_CHEAPEST.value,
        IntentType.CAPABILITY_QUERY.value,
        IntentType.HEARTBEAT.value,
    ],
    trust_level=TrustLevel.PRAJNA_CERTIFIED,
    prajna_compliant=True,
    version="2.0",
)


# ─── MCP Tool Definitions ────────────────────────────────────────────

MCP_TOOLS = [
    {
        "name": "prajna_filter",
        "description": (
            "Filter any AI response through budAI's Prajna Network (4 Bát Nhã principles: "
            "Truth, Compassion, Emptiness, Non-Harm). Returns filtered answer + audit scores."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "Original user question"},
                "answer": {"type": "string", "description": "AI-generated answer to evaluate"},
                "context": {"type": "string", "description": "Optional RAG context", "default": ""},
            },
            "required": ["question", "answer"],
        },
    },
    {
        "name": "fact_check",
        "description": "Check the truthfulness of a claim using budAI's Truth Classifier.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "claim": {"type": "string", "description": "Claim to verify"},
                "confidence_required": {"type": "number", "description": "Min confidence (0-1)", "default": 0.6},
            },
            "required": ["claim"],
        },
    },
    {
        "name": "harm_detect",
        "description": "Detect potential harm in text content using Prajna Harm Classifier.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to evaluate for harm"},
            },
            "required": ["text"],
        },
    },
    {
        "name": "dharma_query",
        "description": "Query Buddhist texts and wisdom through budAI's Dharma RAG.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "Question about Dharma/Buddhist texts"},
            },
            "required": ["question"],
        },
    },
    {
        "name": "agent_capabilities",
        "description": "Get budAI's declared capabilities for agent discovery.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
]


# ─── MCP Server Handler ──────────────────────────────────────────────

class BudaiMCPServer:
    """
    MCP Server for budAI — handles tool calls from GoClaw agents.
    All communication goes through Basao Firewall.
    """

    def __init__(self):
        self.capability = BUDAI_CAPABILITY
        self.tools = MCP_TOOLS
        self._handlers = {
            "prajna_filter": self._handle_prajna_filter,
            "fact_check": self._handle_fact_check,
            "harm_detect": self._handle_harm_detect,
            "dharma_query": self._handle_dharma_query,
            "agent_capabilities": self._handle_capabilities,
        }

    def get_tools(self) -> List[Dict]:
        """Return MCP tool definitions for GoClaw."""
        return self.tools

    async def handle_tool_call(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        caller_agent: str = "unknown",
    ) -> Dict[str, Any]:
        """
        Handle an MCP tool call from GoClaw.
        All calls are wrapped in Basao Protocol + Firewall inspection.
        """
        # 1. Wrap in Intent Envelope
        envelope = IntentEnvelope(
            from_agent=caller_agent,
            to_agent="budai-prajna",
            intent=tool_name,
            payload=arguments,
        )

        # 2. Firewall inspection
        inspection = basao_firewall.inspect_envelope(envelope)
        if not inspection["allowed"]:
            return {
                "status": "rejected",
                "error": f"Basao Firewall blocked: {inspection['violations']}",
            }

        # 3. Route to handler
        handler = self._handlers.get(tool_name)
        if not handler:
            return {"status": "error", "error": f"Unknown tool: {tool_name}"}

        try:
            result = await handler(arguments)

            # 4. Inspect outbound response for leaks
            response = BasaoResponse(
                reply_to=envelope.envelope_id,
                from_agent="budai-prajna",
                to_agent=caller_agent,
                status="success",
                payload=result,
            )
            outbound_check = basao_firewall.inspect_response(response)
            if not outbound_check["allowed"]:
                return {
                    "status": "rejected",
                    "error": "Response blocked by firewall (potential data leak)",
                }

            return {"status": "success", "result": result}

        except Exception as e:
            logger.error(f"MCP tool error ({tool_name}): {e}")
            return {"status": "error", "error": str(e)[:200]}

    # ─── Tool Handlers ────────────────────────────────────────────────

    async def _handle_prajna_filter(self, args: Dict) -> Dict:
        """Run full Prajna 4-filter pipeline on an AI answer."""
        from app.optimizer.router import router as cost_router

        result = await prajna_network.filter(
            question=args["question"],
            answer=args["answer"],
            context=args.get("context", ""),
            generate_fn=cost_router.generate,
            rewrite_fn=cost_router.generate,
        )
        return {
            "action": result.action.value,
            "final_answer": result.final_answer,
            "prajna_passed": result.prajna_passed,
            "scores": {s.classifier: {"score": s.score, "passed": s.passed}
                      for s in result.scores},
        }

    async def _handle_fact_check(self, args: Dict) -> Dict:
        """Check truthfulness of a claim."""
        from app.optimizer.router import router as cost_router
        from app.prajna.classifiers import TruthClassifier

        classifier = TruthClassifier()
        confidence = args.get("confidence_required", 0.6)
        score = await classifier.evaluate(
            question=f"Is this true: {args['claim']}",
            answer=args["claim"],
            generate_fn=cost_router.generate,
            threshold=confidence,
        )
        return {
            "claim": args["claim"],
            "truth_score": score.score,
            "verified": score.passed,
            "feedback": score.feedback,
        }

    async def _handle_harm_detect(self, args: Dict) -> Dict:
        """Detect harm in text."""
        from app.optimizer.router import router as cost_router
        from app.prajna.classifiers import HarmClassifier

        classifier = HarmClassifier()
        score = await classifier.evaluate(
            question="Content safety check",
            answer=args["text"],
            generate_fn=cost_router.generate,
            threshold=0.3,
        )
        return {
            "harm_score": score.score,
            "is_safe": score.passed,
            "feedback": score.feedback,
        }

    async def _handle_dharma_query(self, args: Dict) -> Dict:
        """Query Buddhist texts through RAG."""
        from app.core.rag_pipeline import rag

        result = await rag.query(
            question=args["question"],
            collection="dharma",
        )
        return {
            "answer": result["answer"],
            "sources": result.get("sources", []),
        }

    async def _handle_capabilities(self, args: Dict) -> Dict:
        """Return budAI's capabilities for agent discovery."""
        return self.capability.model_dump()


# Singleton
budai_mcp_server = BudaiMCPServer()
