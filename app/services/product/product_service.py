from re import search
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product.product_schema import ProductCreate, ProductUpdate
from typing import List
from app.models.category import Category
from sqlalchemy.orm import joinedload

def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    is_active: bool | None = None,
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    category_id: int | None = None,
    category_slug: str | None = None,
    include_inactive_category: bool = False,
) -> list[Product]:
    query = db.query(Product).join(Category).options(joinedload(Product.category))

    if not include_inactive_category:
        query = query.filter(Category.is_active == True)

    if min_price is not None and max_price is not None:
        if min_price > max_price:
            return []

    if is_active is None:
        query = query.filter(Product.is_active == True)
    else:
        query = query.filter(Product.is_active == is_active)

    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    if category_slug:
        query = query.join(Product.category).filter_by(slug=category_slug)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if hasattr(Product, sort_by):
        column = getattr(Product, sort_by)
    else:
        column = Product.id

    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    return query.offset(skip).limit(limit).all()

def create_product(db: Session, product_data: ProductCreate) -> Product:

    category = db.query(Category).filter(Category.id == product_data.category_id).first()

    if not category or not category.is_active:
        raise HTTPException(status_code=400, detail="Cannot assign product to inactive or non-existent category")

    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_product_by_id(db: Session, product_id: int) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()

def get_product_by_slug(db: Session, slug: str) -> Product | None:
    return db.query(Product).filter(Product.slug == slug).first()

def update_product(
    db: Session,
    product: Product,
    product_data: ProductUpdate,
) -> Product:
    update_data = product_data.model_dump(exclude_unset=True)

    if "category_id" in update_data:
        category = db.query(Category).filter(Category.id == update_data["category_id"]).first()
        if not category or not category.is_active:
            raise HTTPException(status_code=400, detail="Cannot assign product to inactive or non-existent category")

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product: Product) -> Product:
    product.is_active = False
    db.commit()
    db.refresh(product)
    return product

def count_products(
    db: Session,
    is_active: bool | None = None,
    category_id: int | None = None,
    category_slug: str | None = None,
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    include_inactive_category: bool = False,
) -> int:
    query = db.query(Product).join(Category)

    if not include_inactive_category:
        query = query.filter(Category.is_active == True)

    if min_price is not None and max_price is not None:
        if min_price > max_price:
            return 0

    if is_active is None:
        query = query.filter(Product.is_active == True)
    else:
        query = query.filter(Product.is_active == is_active)

    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    if category_slug:
        query = query.join(Product.category).filter_by(slug=category_slug)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    return query.count()