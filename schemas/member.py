from pydantic import (
    BaseModel,
    EmailStr,
    Field
)


class MemberCreate(BaseModel):

    name: str = Field(..., min_length=3)

    email: EmailStr

    phone: str = Field(..., min_length=10, max_length=10)

    membership_type: str

    status: str
