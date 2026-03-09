"""
GoClaw Bridge — HTTP client to communicate with GoClaw agents.
budAI can delegate tasks to GoClaw through Basao Protocol.
"""

import logging
from typing import Any, Dict, List, Optional

import httpx

from app.basao.protocol import IntentEnvelope, BasaoResponse, AgentCapability
from app.basao.firewall import basao_firewall

logger = logging.getLogger("budai.basao.bridge")


class GoclawBridge:
    """
    HTTP bridge to GoClaw multi-agent gateway.
    Enables budAI to delegate tasks to GoClaw agents through Basao Protocol.
    """

    def __init__(
        self,
        goclaw_url: str = "http://localhost:18790",
        api_token: Optional[str] = None,
    ):
        self.goclaw_url = goclaw_url.rstrip("/")
        self.api_token = api_token
        self._known_agents: Dict[str, AgentCapability] = {}

    def _headers(self) -> Dict[str, str]:
        """Build HTTP headers."""
        headers = {"Content-Type": "application/json"}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        return headers

    async def discover_agents(self) -> List[AgentCapability]:
        """
        Discover available GoClaw agents.
        Returns capabilities without database info.
        """
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"{self.goclaw_url}/api/agents",
                    headers=self._headers(),
                )
                resp.raise_for_status()
                agents_data = resp.json()

            capabilities = []
            for agent in agents_data.get("agents", []):
                cap = AgentCapability(
                    agent_id=agent.get("slug", agent.get("id", "unknown")),
                    agent_name=agent.get("name", "Unknown Agent"),
                    capabilities=self._infer_capabilities(agent),
                    trust_level="discovered",
                    prajna_compliant=False,
                )
                capabilities.append(cap)
                self._known_agents[cap.agent_id] = cap

            logger.info(f"🌉 Discovered {len(capabilities)} GoClaw agents")
            return capabilities

        except Exception as e:
            logger.error(f"🌉 GoClaw discovery failed: {e}")
            return []

    async def delegate(
        self,
        envelope: IntentEnvelope,
        target_agent: str,
    ) -> BasaoResponse:
        """
        Delegate a task to a GoClaw agent through Basao Protocol.
        """
        # 1. Firewall check outbound
        inspection = basao_firewall.inspect_envelope(envelope)
        if not inspection["allowed"]:
            return BasaoResponse(
                reply_to=envelope.envelope_id,
                from_agent="budai-prajna",
                to_agent=target_agent,
                status="rejected",
                payload={"error": f"Firewall blocked: {inspection['violations']}"},
            )

        # 2. Map intent to GoClaw message
        goclaw_message = self._map_to_goclaw(envelope)

        # 3. Send to GoClaw
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                resp = await client.post(
                    f"{self.goclaw_url}/api/chat",
                    headers=self._headers(),
                    json=goclaw_message,
                )
                resp.raise_for_status()
                result = resp.json()

            # 4. Firewall check inbound response
            response = BasaoResponse(
                reply_to=envelope.envelope_id,
                from_agent=target_agent,
                to_agent="budai-prajna",
                status="success",
                payload={"answer": result.get("content", result.get("message", ""))},
            )

            inbound_check = basao_firewall.inspect_response(response)
            if not inbound_check["allowed"]:
                response.status = "rejected"
                response.payload = {"error": "Inbound response blocked by firewall"}

            return response

        except Exception as e:
            logger.error(f"🌉 GoClaw delegation failed: {e}")
            return BasaoResponse(
                reply_to=envelope.envelope_id,
                from_agent=target_agent,
                to_agent="budai-prajna",
                status="error",
                payload={"error": str(e)[:200]},
            )

    async def health_check(self) -> Dict[str, Any]:
        """Check if GoClaw gateway is reachable."""
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(
                    f"{self.goclaw_url}/api/health",
                    headers=self._headers(),
                )
                return {"status": "connected", "goclaw_url": self.goclaw_url}
        except Exception as e:
            return {"status": "disconnected", "error": str(e)[:100]}

    def _map_to_goclaw(self, envelope: IntentEnvelope) -> Dict:
        """Map Basao Intent Envelope to GoClaw API format."""
        # GoClaw expects a chat-like message
        payload = envelope.payload

        if envelope.intent == "delegate":
            return {
                "agent": envelope.to_agent,
                "message": payload.get("task", payload.get("question", "")),
                "session_id": envelope.trace_id or envelope.envelope_id,
            }

        # Default: send as chat message
        message = payload.get("question", payload.get("claim", payload.get("text", "")))
        return {
            "agent": envelope.to_agent,
            "message": f"[Basao/{envelope.intent}] {message}",
            "session_id": envelope.trace_id or envelope.envelope_id,
        }

    def _infer_capabilities(self, agent_data: Dict) -> List[str]:
        """Infer agent capabilities from GoClaw agent config."""
        caps = ["delegate"]
        tools = agent_data.get("tools", [])
        if "web_search" in tools or "web_fetch" in tools:
            caps.append("fact_check")
        if "memory_search" in tools or "skill_search" in tools:
            caps.append("knowledge_query")
        if "evaluate_loop" in tools:
            caps.append("prajna_filter")
        return caps


# Default bridge (not connected until configured)
goclaw_bridge = GoclawBridge()
