from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal

from models.member import Member

from schemas.member import MemberCreate

from services.subscription_service import valid_phone

router = APIRouter(
    prefix="/members",
    tags=["Members"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_member(
    member: MemberCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Member).filter(
        Member.email == member.email
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Member email already exists."
        )

    if not valid_phone(member.phone):

        raise HTTPException(
            status_code=400,
            detail="Phone number must contain exactly 10 digits."
        )

    new_member = Member(
        name=member.name,
        email=member.email,
        phone=member.phone,
        membership_type=member.membership_type,
        status=member.status
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member


@router.get("/")
def get_members(
    search: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Member)

    if search:

        query = query.filter(
            (Member.name.contains(search)) |
            (Member.email.contains(search))
        )

    total = query.count()

    members = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": members
    }


@router.get("/{member_id}")
def get_member(
    member_id: int,
    db: Session = Depends(get_db)
):

    member = db.query(Member).filter(
        Member.id == member_id
    ).first()

    if not member:

        raise HTTPException(
            status_code=404,
            detail="Member not found."
        )

    return member


@router.put("/{member_id}")
def update_member(
    member_id: int,
    member: MemberCreate,
    db: Session = Depends(get_db)
):

    db_member = db.query(Member).filter(
        Member.id == member_id
    ).first()

    if not db_member:

        raise HTTPException(
            status_code=404,
            detail="Member not found."
        )

    db_member.name = member.name
    db_member.email = member.email
    db_member.phone = member.phone
    db_member.membership_type = member.membership_type
    db_member.status = member.status

    db.commit()

    return {
        "message": "Member updated successfully."
    }


@router.delete("/{member_id}")
def delete_member(
    member_id: int,
    db: Session = Depends(get_db)
):

    member = db.query(Member).filter(
        Member.id == member_id
    ).first()

    if not member:

        raise HTTPException(
            status_code=404,
            detail="Member not found."
        )

    db.delete(member)

    db.commit()

    return {
        "message": "Member deleted successfully."
    }
