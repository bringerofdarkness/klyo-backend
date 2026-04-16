from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.core.response import success_response
from app.api.deps import get_current_user
from app.core.permissions import require_role
from app.schemas.order.order_schema import OrderCreate, OrderStatusUpdate
from app.services.order.order_service import (
    create_order,
    get_user_orders,
    get_all_orders,
    cancel_order,
    update_order_status,
)

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/")
def create_order_endpoint(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    order = create_order(db=db, user_id=current_user.id, order_data=order_data)
    return success_response(data=order, message="Order created successfully")

@router.get("/")
def get_all_orders_endpoint(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    orders = get_all_orders(db=db)
    return success_response(data=orders, message="All orders fetched successfully")

@router.get("/my")
def get_my_orders_endpoint(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    orders = get_user_orders(db=db, user_id=current_user.id)
    return success_response(data=orders, message="Orders fetched successfully")


@router.delete("/{order_id}")
def cancel_order_endpoint(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    cancel_order(db=db, order_id=order_id, user_id=current_user.id)
    return success_response(data={"order_id": order_id}, message="Order cancelled successfully")


@router.patch("/{order_id}/status")
def update_order_status_endpoint(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    order = update_order_status(
        db=db,
        order_id=order_id,
        status=status_data.status
    )
    return success_response(data=order, message="Order status updated successfully")