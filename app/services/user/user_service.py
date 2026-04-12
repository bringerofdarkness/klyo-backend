from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from passlib.context import CryptContext
from app.schemas.user.user_schema import UserRole

from app.models.user import User
from app.schemas.user.user_schema import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(
    db: Session,
    user: UserCreate
) -> User:
    """
    Create a new user using schema object.
    """

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(user.password)

    new_user = User(
    name=user.name,
    email=user.email,
    hashed_password=hashed_password,
    # Public registration always creates customer users
    role=UserRole.customer
)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_all_users(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None,
    role: str | None = None,
    sort_by: str = "id",
    order: str = "asc",
    email: str | None = None
) -> list[User]:

    query = db.query(User)

    if search:
     query = query.filter(
        or_(
            User.name.ilike(f"%{search}%"),
            User.email.ilike(f"%{search}%"),
            User.role.ilike(f"%{search}%")
        )
    )
    
    if role:
        query = query.filter(User.role == role)

    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))

    if hasattr(User, sort_by):
        column = getattr(User, sort_by)
        if order == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))
    else:
        query = query.order_by(asc(User.id))
    total = query.count()

    users = query.offset(skip).limit(limit).all()

    return {
    "users": users,
    "total": total,
    "skip": skip,
    "limit": limit
}

def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Fetch a single user by ID.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


def update_user(
    db: Session,
    user_id: int,
    user_data: UserUpdate
) -> User:
    """
    Update a user's editable fields.
    """

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user_data.name is not None:
        user.name = user_data.name

    if user_data.password is not None:
        user.hashed_password = pwd_context.hash(user_data.password)

    db.commit()
    db.refresh(user)

    return user

def delete_user(db: Session, user_id: int) -> dict:
    """
    Delete a user by ID.
    """

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}

def authenticate_user(db: Session, email: str, password: str) -> User:
    """
    Authenticate user by email and password.
    """

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password (IMPORTANT: not hash again)
    if not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return user