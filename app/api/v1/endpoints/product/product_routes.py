from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.response import success_response
from app.db.dependencies import get_db

from app.services.product.product_service import create_product, get_products, count_products
from app.schemas.product.product_schema import ProductCreate, ProductUpdate
from app.core.permissions import require_role

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/")
def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db)):
    created_product = create_product(db=db, product_data=product)
    return success_response(data=created_product, message="Product created successfully")


@router.get("/")
def get_products_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("id"),
    order: str = Query("asc"),
    is_active: bool | None = Query(None),
    category_id: int | None = Query(None),
    category_slug: str | None = Query(None),
    search: str | None = Query(None),
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    include_inactive_category: bool = Query(False),
    db: Session = Depends(get_db),
):
    products = get_products(
    db=db,
    skip=skip,
    limit=limit,
    sort_by=sort_by,
    order=order,
    is_active=is_active,
    category_id=category_id,
    category_slug=category_slug,
    search=search,
    min_price=min_price,
    max_price=max_price,
    include_inactive_category=include_inactive_category,
)
    
    total = count_products(
    db=db,
    is_active=is_active,
    category_id=category_id,
    category_slug=category_slug,
    search=search,
    min_price=min_price,
    max_price=max_price,
    include_inactive_category=include_inactive_category,
)
    return success_response(
        data={
            "items": products,
            "total": total,
            "skip": skip,
            "limit": limit,
            "page": (skip // limit) + 1,
            "pages": (total + limit - 1) // limit,
    },
    message="Products fetched successfully",
)

@router.get("/slug/{slug}")
def get_product_by_slug_endpoint(
    slug: str,
    db: Session = Depends(get_db),
):
    from app.services.product.product_service import get_product_by_slug

    product = get_product_by_slug(db=db, slug=slug)

    if not product:
        return success_response(data=None, message="Product not found")

    return success_response(data=product, message="Product fetched successfully")

@router.get("/{product_id}")
def get_product_by_id_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
):
    from app.services.product.product_service import get_product_by_id

    product = get_product_by_id(db=db, product_id=product_id)

    if not product:
        return success_response(data=None, message="Product not found")

    return success_response(data=product, message="Product fetched successfully")

@router.put("/{product_id}")
def update_product_endpoint(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    from app.services.product.product_service import get_product_by_id, update_product

    product = get_product_by_id(db=db, product_id=product_id)

    if not product:
        return success_response(data=None, message="Product not found")

    updated_product = update_product(db=db, product=product, product_data=product_data)
    return success_response(data=updated_product, message="Product updated successfully")

@router.delete("/{product_id}")
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin")),
):
    from app.services.product.product_service import get_product_by_id, delete_product

    product = get_product_by_id(db=db, product_id=product_id)

    if not product:
        return success_response(data=None, message="Product not found")

    delete_product(db=db, product=product)
    return success_response(data=None, message="Product deactivated successfully")