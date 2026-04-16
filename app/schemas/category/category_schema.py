from pydantic import BaseModel, Field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.product.product_schema import ProductResponse

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    slug: str | None = Field(default=None, max_length=120)
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    is_active: bool | None = None


class CategoryResponse(CategoryBase):
    id: int
    products: list["ProductResponse"] = []
    

    class Config:
        from_attributes = True