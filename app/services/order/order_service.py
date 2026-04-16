from app.models import order
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order.order_schema import OrderCreate


def create_order(db: Session, user_id: int, order_data: OrderCreate) -> Order:
    order = Order(user_id=user_id, total_price=0)
    db.add(order)
    db.flush()

    total_price = 0

    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

        if not product.is_active:
            raise HTTPException(status_code=400, detail=f"Product {item.product_id} is inactive")

        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.id}")

        item_price = product.price * item.quantity
        total_price += item_price

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price,
        )

        db.add(order_item)

        product.stock -= item.quantity

    order.total_price = total_price

    db.commit()

    order = (
    db.query(Order)
    .options(joinedload(Order.items).joinedload(OrderItem.product))
    .filter(Order.id == order.id)
    .first()
    )

    return order

def get_user_orders(db: Session, user_id: int) -> list[Order]:
    from sqlalchemy.orm import joinedload

    return (
        db.query(Order)
        .options(joinedload(Order.items).joinedload(OrderItem.product))
        .filter(Order.user_id == user_id)
        .all()
    )

def get_all_orders(
    db: Session,
    status: str | None = None,
    user_id: int | None = None
) -> list[Order]:
    from sqlalchemy.orm import joinedload

    query = (
        db.query(Order)
        .options(joinedload(Order.items).joinedload(OrderItem.product))
    )

    if status:
        query = query.filter(Order.status == status)

    if user_id:
        query = query.filter(Order.user_id == user_id)

    return query.all()

def cancel_order(db: Session, order_id: int, user_id: int) -> Order:
    order = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed to cancel this order")

    if order.status == "cancelled":
        raise HTTPException(status_code=400, detail="Order already cancelled")

    # restore stock
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock += item.quantity

    # 🔥 instead of delete
    order.status = "cancelled"

    db.commit()
    db.refresh(order)

    return order

def update_order_status(db: Session, order_id: int, status: str) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status == "cancelled":
        raise HTTPException(status_code=400, detail="Cancelled orders cannot be updated")

    # optional: restrict allowed values
    allowed_statuses = ["pending", "shipped", "delivered", "cancelled"]
    if status not in allowed_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    if order.status == "delivered":
        raise HTTPException(status_code=400, detail="Delivered orders cannot be updated")
    
    status_flow = ["pending", "shipped", "delivered"]

    if order.status in status_flow and status in status_flow:
        if status_flow.index(status) < status_flow.index(order.status):
            raise HTTPException(status_code=400, detail="Cannot move order status backward")
    
    if status == "cancelled" and order.status != "pending":
        raise HTTPException(status_code=400, detail="Only pending orders can be cancelled")

   
    
    if order.status == status:
        raise HTTPException(status_code=400, detail="Order already has this status")

    order.status = status

    if status == "delivered":
        from datetime import datetime
        order.delivered_at = datetime.utcnow()

    db.commit()
    db.refresh(order)

    return order