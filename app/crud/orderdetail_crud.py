from sqlalchemy.orm import Session
from .. import models, schemas
from ..logging_config import logger
from fastapi import HTTPException

def get_orderdetails(db: Session, skip: int = 0, limit: int = 10):
    logger.info(f"CRUD: Fetching order details skip={skip}, limit={limit}")
    return db.query(models.OrderDetail).offset(skip).limit(limit).all()

def get_orderdetail(db: Session, order_number: int, product_code: str):
    db_item = db.query(models.OrderDetail).filter(
        models.OrderDetail.orderNumber == order_number,
        models.OrderDetail.productCode == product_code
    ).first()
    if not db_item:
        logger.warning(f"CRUD: OrderDetail {order_number}/{product_code} not found")
        raise HTTPException(status_code=404, detail="Order detail line item not found")
    return db_item

def get_details_by_order(db: Session, order_number: int):
    return db.query(models.OrderDetail).filter(models.OrderDetail.orderNumber == order_number).all()

def get_details_by_product(db: Session, product_code: str):
    return db.query(models.OrderDetail).filter(models.OrderDetail.productCode == product_code).all()

def create_orderdetail(db: Session, data: schemas.orderdetail_schemas.OrderDetailCreate):
    db_item = models.OrderDetail(**data.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_orderdetail(db: Session, order_number: int, product_code: str, data: schemas.orderdetail_schemas.OrderDetailUpdate):
    db_item = get_orderdetail(db, order_number, product_code)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_orderdetail(db: Session, order_number: int, product_code: str):
    db_item = get_orderdetail(db, order_number, product_code)
    db.delete(db_item)
    db.commit()
    return {"detail": "Line item removed from order"}