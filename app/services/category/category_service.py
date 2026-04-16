from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.category import Category
from app.schemas.category.category_schema import CategoryCreate, CategoryUpdate


def create_category(db: Session, category_data: CategoryCreate) -> Category:
    data = category_data.model_dump()

    if not data.get("slug"):
        data["slug"] = data["name"].lower().replace(" ", "-")

    existing = db.query(Category).filter(Category.name == data["name"]).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category with this name already exists")

    existing_slug = db.query(Category).filter(Category.slug == data["slug"]).first()
    if existing_slug:
        raise HTTPException(status_code=400, detail="Category with this slug already exists")

    category = Category(**data)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_categories(db: Session, include_inactive: bool = False) -> list[Category]:
    query = db.query(Category)

    if not include_inactive:
        query = query.filter(Category.is_active == True)

    return query.all()


def get_category_by_id(db: Session, category_id: int) -> Category | None:
    from sqlalchemy.orm import joinedload

    return (
        db.query(Category)
        .options(joinedload(Category.products))
        .filter(Category.id == category_id)
        .first()
    )


def update_category(db: Session, category_id: int, category_data: CategoryUpdate) -> Category:
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    update_data = category_data.model_dump(exclude_unset=True)

    if "name" in update_data and "slug" not in update_data:
        update_data["slug"] = update_data["name"].lower().replace(" ", "-")

    if "name" in update_data:
        existing = (
            db.query(Category)
            .filter(Category.name == update_data["name"], Category.id != category_id)
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Category with this name already exists")

    if "slug" in update_data:
        existing_slug = (
            db.query(Category)
            .filter(Category.slug == update_data["slug"], Category.id != category_id)
            .first()
        )
        if existing_slug:
            raise HTTPException(status_code=400, detail="Category with this slug already exists")

    for field, value in update_data.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> Category:
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.is_active = False

    db.commit()
    db.refresh(category)
    return category