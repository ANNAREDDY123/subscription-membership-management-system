from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Date,
    ForeignKey
)

from database import Base


class Payment(Base):

    __tablename__ = "payments"

    id = Column(
        Integer,
        primary_key=True
    )

    subscription_id = Column(
        Integer,
        ForeignKey("subscriptions.id")
    )

    amount = Column(Float)

    payment_date = Column(Date)

    payment_method = Column(String)
