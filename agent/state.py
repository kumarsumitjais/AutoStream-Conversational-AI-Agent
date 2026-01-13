from pydantic import BaseModel


class AgentState(BaseModel):
    user_input: str = ""

    intent: str = ""
    intent_confidence: float = 0.0

    lead_step: str = ""
    name: str = ""
    email: str = ""
    platform: str = ""

    selected_plan: str = ""   # ⭐ NEW

    response: str = ""
    lead_captured: bool = False
