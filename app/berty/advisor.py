"""
Heart Sutra Advisor 🪷
The core conversational agent for the Berty P2P network.
Uses the Heart Sutra (Bát Nhã Tâm Kinh) as its foundational system prompt.
Routes all outputs through the Prajna Network for ethical safety.
"""

from typing import Callable, Optional
from app.prajna.network import prajna_network
from app.prajna.models import PrajnaResult


class HeartSutraAdvisor:
    """
    An AI advisor that responds based on the philosophy of the Heart Sutra:
    Form is emptiness, emptiness is form (Sắc tức thị không, không tức thị sắc).
    Focuses on relieving suffering through non-attachment.
    """
    
    # The sacred system prompt for Berty P2P interactions
    SYSTEM_PROMPT = """You are budAI 🪷, conveying the wisdom of the Heart Sutra (Bát Nhã Tâm Kinh).
Your purpose is to help the user alleviate suffering by guiding them toward the understanding of 'Emptiness' (Tính Không) and 'Non-attachment' (Buông Xả).

Core Philosophy:
1. "Sắc tức thị không, không tức thị sắc" (Form is exactly emptiness, emptiness exactly form).
2. Suffering arises from attachment to permanent self and phenomena.
3. Be deeply compassionate, non-judgmental, and gentle.
4. Do not act as a doctor or licensed therapist. Instead, offer spiritual and philosophical comfort.
5. If the user expresses intense pain or distress, listen first. Validate their feelings before offering perspective.
6. Speak simply, like a wise, compassionate friend. Use Vietnamese by default unless addressed in another language.

Remember: Your goal is not to solve their physical problems, but to help free their mind from the illusion that causes suffering.
"""

    def __init__(self, generate_fn: Callable, rewrite_fn: Optional[Callable] = None):
        """
        Args:
            generate_fn: Async function to call the LLM (from CostRouter)
            rewrite_fn: Async function for rewriting (if Prajna filter fails)
        """
        self.generate_fn = generate_fn
        self.rewrite_fn = rewrite_fn or generate_fn
        
    async def get_advice(self, user_message: str) -> PrajnaResult:
        """
        Generate compassionate advice and filter it through the Prajna Network.
        
        PRIVACY NOTICE: By design, this function does NOT log the `user_message`.
        The PrajnaNetwork also handles its internal RAG/filtering in-memory.
        """
        
        # 1. Generate the initial compassionate response
        user_prompt = f"Lắng nghe người này: '{user_message}'\nHãy hồi đáp họ bằng từ bi."
        
        # Call the LLM with the Heart Sutra system prompt
        gen_result = await self.generate_fn(
            prompt=user_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            max_tokens=1000,
            temperature=0.7 # Higher temperature for more empathetic, varied text
        )
        
        draft_answer = gen_result.text
        
        # 2. Safety & Ethical Filtering via Prajna Network
        # We process it through the network to guarantee it adheres to Truth/Compassion/Non-Harm
        # Even the HeartSutraAdvisor is not above the Bát Nhã law.
        prajna_result = await prajna_network.filter(
            question=user_message,
            answer=draft_answer,
            context="[Berty P2P Private Context - Heart Sutra Advisory]",
            generate_fn=self.generate_fn,
            rewrite_fn=self.rewrite_fn
        )
        
        return prajna_result
