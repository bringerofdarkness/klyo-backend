from app.core.permissions import require_role
from app.models import category
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session


from app.core.response import success_response
from app.db.dependencies import get_db
from app.schemas.category.category_schema import CategoryCreate, CategoryUpdate
from app.services.category.category_service import create_category, update_category, delete_category


router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/")
def create_category_endpoint(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    created_category = create_category(db=db, category_data=category)
    return success_response(data=created_category, message="Category created successfully")


@router.get("/")
def get_categories_endpoint(
    include_inactive: bool = False,
    db: Session = Depends(get_db),
):
    from app.services.category.category_service import get_categories



    categories = get_categories(db=db, include_inactive=include_inactive)
    return success_response(data=categories, message="Categories fetched successfully")

@router.get("/all")
def get_all_categories_endpoint(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    from app.services.category.category_service import get_categories

    categories = get_categories(db=db, include_inactive=True)
    return success_response(data=categories, message="All categories fetched successfully")

@router.get("/{category_id}")
def get_category_by_id_endpoint(
    category_id: int,
    db: Session = Depends(get_db),
):
    from app.services.category.category_service import get_category_by_id

    category = get_category_by_id(db=db, category_id=category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return success_response(data=category, message="Category fetched successfully")

@router.put("/{category_id}", status_code=status.HTTP_200_OK)
def update_category_endpoint(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    updated_category = update_category(db=db, category_id=category_id, category_data=category_data)
    return success_response(data=updated_category, message="Category updated successfully")

@router.delete("/{category_id}")
def delete_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    deleted_category = delete_category(db=db, category_id=category_id)
    return success_response(data=deleted_category, message="Category deleted successfully")