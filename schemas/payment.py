from pydantic import (
    BaseModel,
    Field
)

from datetime import date


class PaymentCreate(BaseModel):

    subscription_id: int

    amount: float = Field(..., gt=0)

    payment_date: date

    payment_method: str = Field(..., min_length=3)
