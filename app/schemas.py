from pydantic import BaseModel, Field
from typing import Optional

class PlanGroupFromStoppedRequest(BaseModel):
    group_name: str = Field(..., min_length=2, max_length=60)
    days: int = 7
    top_n: int = 5
    speed_threshold: float = 1.0

class ConfirmGroupFromStoppedRequest(PlanGroupFromStoppedRequest):
    confirm_token: str