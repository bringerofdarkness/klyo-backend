# Import all models here so SQLAlchemy knows them before table creation
from app.models.user import User

__all__ = ["User"]