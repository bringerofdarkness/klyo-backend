
from sqlalchemy.orm import Session
from app.core.response import success_response
from app.core.security import create_access_token
from fastapi import APIRouter, Depends, Form
from fastapi import APIRouter, Depends, Form, HTTPException
from app.api.deps import get_current_user
from app.models.user import User
from app.core.permissions import require_role
from app.db.dependencies import get_db
from app.schemas.common import APIResponse

from app.schemas.user.user_schema import (
    MessageResponse,
    UserCreate,
    UserCreateResponse,
    UserListResponse,
    UserUpdate,
    TokenResponse,
)
from app.services.user.user_service import (
    create_user,
    delete_user,
    get_all_users,
    get_user_by_id,
    update_user,
    authenticate_user,
)

router = APIRouter()

@router.post("/register", response_model=APIResponse[UserCreateResponse])
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    created_user = create_user(db=db, user=user)

    return success_response(
        data=created_user,
        message="User registered successfully"
    )



@router.post("/login", response_model=TokenResponse)
def login_user(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db=db,
        email=username,
        password=password
    )

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=APIResponse[UserCreateResponse])
def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user
    """
    return success_response(
        data=current_user,
        message="Current user fetched successfully"
    )

@router.get("/admin-only", response_model=APIResponse[MessageResponse])
def admin_only_route(current_user: User = Depends(require_role("admin"))):
    """
    Admin-only test route
    """
    return success_response(
    data={"message": f"Welcome admin {current_user.name}"},
    message="Admin access granted"
)

@router.get("/{user_id}", response_model=APIResponse[UserCreateResponse])

def get_single_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = get_user_by_id(db=db, user_id=user_id)

    return success_response(
        data=user,
        message="User fetched successfully"
    )


@router.get("/", response_model=APIResponse[UserListResponse])
def list_users(
    skip: int = 0,
    limit: int = 10,
    search: str | None = None,
    role: str | None = None,
    email: str | None = None,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    if order not in ["asc", "desc"]:
        raise HTTPException(
        status_code=400,
        detail="order must be either 'asc' or 'desc'"
    )
    if order not in ["asc", "desc"]:
        raise HTTPException(
        status_code=400,
        detail="order must be either 'asc' or 'desc'"
    )
    allowed_sort_fields = ["id", "name", "email", "role", "created_at"]

    if sort_by not in allowed_sort_fields:
     raise HTTPException(
        status_code=400,
        detail=f"sort_by must be one of: {', '.join(allowed_sort_fields)}"
    )
    if limit < 1 or limit > 100:
        raise HTTPException(
        status_code=400,
        detail="limit must be between 1 and 100"
    )
    if skip < 0:
        raise HTTPException(
        status_code=400,
        detail="skip cannot be negative"
    )
    users = get_all_users(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        role=role,
        email=email,
        sort_by=sort_by,
        order=order
    )

    return success_response(
        data=users,
        message="Users fetched successfully"
    )


@router.patch("/{user_id}", response_model=APIResponse[UserCreateResponse])
def update_single_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a single user
    """
    updated_user = update_user(
    db=db,
    user_id=user_id,
    user_data=user_data
)

    return success_response(
    data=updated_user,
    message="User updated successfully"
)


@router.delete("/{user_id}", response_model=APIResponse[MessageResponse])
def delete_single_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    """
    Delete a single user
    """
    result = delete_user(db=db, user_id=user_id)
    return success_response(
        data=result,
        message="User deleted successfully"
    )