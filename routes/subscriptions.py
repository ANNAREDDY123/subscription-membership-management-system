from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal

from models.subscription import Subscription
from models.member import Member

from schemas.subscription import SubscriptionCreate

from services.subscription_service import (
    valid_subscription_status,
    valid_dates
)

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_subscription(
    subscription: SubscriptionCreate,
    db: Session = Depends(get_db)
):

    member = db.query(Member).filter(
        Member.id == subscription.member_id
    ).first()

    if not member:

        raise HTTPException(
            status_code=404,
            detail="Member not found."
        )

    active = db.query(Subscription).filter(
        Subscription.member_id == subscription.member_id,
        Subscription.status == "Active"
    ).first()

    if active:

        raise HTTPException(
            status_code=400,
            detail="Member already has an active subscription."
        )

    if not valid_dates(
        subscription.start_date,
        subscription.end_date
    ):

        raise HTTPException(
            status_code=400,
            detail="End date must be greater than start date."
        )

    if not valid_subscription_status(subscription.status):

        raise HTTPException(
            status_code=400,
            detail="Invalid subscription status."
        )

    new_subscription = Subscription(
        member_id=subscription.member_id,
        plan_name=subscription.plan_name,
        start_date=subscription.start_date,
        end_date=subscription.end_date,
        amount=subscription.amount,
        status=subscription.status
    )

    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)

    return new_subscription


@router.get("/")
def get_subscriptions(
    status: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Subscription)

    if status:
        query = query.filter(
            Subscription.status == status
        )

    total = query.count()

    subscriptions = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": subscriptions
    }


@router.get("/{subscription_id}")
def get_subscription(
    subscription_id: int,
    db: Session = Depends(get_db)
):

    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not subscription:

        raise HTTPException(
            status_code=404,
            detail="Subscription not found."
        )

    return subscription


@router.put("/{subscription_id}")
def update_subscription(
    subscription_id: int,
    subscription: SubscriptionCreate,
    db: Session = Depends(get_db)
):

    db_subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not db_subscription:

        raise HTTPException(
            status_code=404,
            detail="Subscription not found."
        )

    if db_subscription.status == "Expired":

        raise HTTPException(
            status_code=400,
            detail="Expired subscriptions cannot be updated."
        )

    db_subscription.plan_name = subscription.plan_name
    db_subscription.start_date = subscription.start_date
    db_subscription.end_date = subscription.end_date
    db_subscription.amount = subscription.amount
    db_subscription.status = subscription.status

    db.commit()

    return {
        "message": "Subscription updated successfully."
    }
