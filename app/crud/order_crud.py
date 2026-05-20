from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from .. import models
from ..schemas import order_schemas
from ..logging_config import logger

def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Order).offset(skip).limit(limit).all()

def get_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.orderNumber == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

def get_orders_by_customer(db: Session, customer_id: int):
    # Note: Returns [] if no orders, no 404 raised here as per Page 14
    return db.query(models.Order).filter(models.Order.customerNumber == customer_id).all()

def create_order(db: Session, order_data: order_schemas.OrderCreate):
    db_order = models.Order(**order_data.model_dump())
    db.add(db_order)
    try:
        db.commit()
        db.refresh(db_order)
        return db_order
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=422, detail="Invalid customerNumber or duplicate orderNumber.")

def update_order(db: Session, order_id: int, order_data: order_schemas.OrderUpdate):
    db_order = get_order(db, order_id)
    update_dict = order_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    try:
        db.delete(db_order)
        db.commit()
        return {"detail": "Order deleted"}
    except IntegrityError:
        db.rollback()
        # Requirement Page 14: Return 409 Conflict for orderdetails reference
        raise HTTPException(
            status_code=409, 
            detail="Conflict: Cannot delete order because it has line items (orderdetails)."
        )