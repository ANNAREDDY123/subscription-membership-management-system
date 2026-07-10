from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey
)

from database import Base


class Subscription(Base):

    __tablename__ = "subscriptions"

    id = Column(
        Integer,
        primary_key=True
    )

    member_id = Column(
        Integer,
        ForeignKey("members.id")
    )

    plan_name = Column(String)

    start_date = Column(Date)

    end_date = Column(Date)

    amount = Column(Float)

    status = Column(String)
