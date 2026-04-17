from fastapi import APIRouter

from app.api.v1.endpoints.product.product_routes import router as product_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.user.user_routes import router as user_router
from app.api.v1.endpoints.category.category_routes import router as category_router
from app.api.v1.endpoints.order.order_routes import router as order_router

api_router = APIRouter(prefix="/api/v1")

# Product routes
api_router.include_router(product_router)

# Health route
api_router.include_router(health_router, prefix="/hello", tags=["Health"])

# User route
api_router.include_router(user_router, prefix="/user", tags=["User"])

# Category route
api_router.include_router(category_router, prefix="/category", tags=["Category"])

# Order route
api_router.include_router(order_router, prefix="/order", tags=["Order"])