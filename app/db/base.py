from sqlalchemy.orm import declarative_base

# Base class for all database models
Base = declarative_base()

# Import models AFTER Base is created
from app.models.order import Order, OrderItem