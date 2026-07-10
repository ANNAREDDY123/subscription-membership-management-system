from pydantic import (
    BaseModel,
    Field
)

from datetime import date


class SubscriptionCreate(BaseModel):

    member_id: int

    plan_name: str = Field(..., min_length=2)

    start_date: date

    end_date: date

    amount: float = Field(..., gt=0)

    status: str
