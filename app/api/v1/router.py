from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.user.user_routes import router as user_router

api_router = APIRouter()

# Health route
api_router.include_router(health_router, prefix="/hello", tags=["Health"])

# User route
api_router.include_router(user_router, prefix="/user", tags=["User"])