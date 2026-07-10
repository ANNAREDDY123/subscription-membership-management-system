from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal

from models.payment import Payment
from models.subscription import Subscription

from schemas.payment import PaymentCreate

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):

    subscription = db.query(Subscription).filter(
        Subscription.id == payment.subscription_id
    ).first()

    if not subscription:

        raise HTTPException(
            status_code=404,
            detail="Subscription not found."
        )

    new_payment = Payment(
        subscription_id=payment.subscription_id,
        amount=payment.amount,
        payment_date=payment.payment_date,
        payment_method=payment.payment_method
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return new_payment


@router.get("/")
def get_payments(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Payment)

    total = query.count()

    payments = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": payments
    }


@router.get("/members/{member_id}/payments")
def member_payments(
    member_id: int,
    db: Session = Depends(get_db)
):

    payments = db.query(Payment).join(
        Subscription,
        Payment.subscription_id == Subscription.id
    ).filter(
        Subscription.member_id == member_id
    ).all()

    return payments
