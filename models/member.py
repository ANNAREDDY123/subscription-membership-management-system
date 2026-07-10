from sqlalchemy import (
    Column,
    Integer,
    String
)

from database import Base


class Member(Base):

    __tablename__ = "members"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(String)

    email = Column(
        String,
        unique=True
    )

    phone = Column(String)

    membership_type = Column(String)

    status = Column(String)
