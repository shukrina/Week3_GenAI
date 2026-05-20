from sqlalchemy.orm import Session
from .. import models, schemas
from ..logging_config import logger
from fastapi import HTTPException

def get_payments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Payment).offset(skip).limit(limit).all()

def get_payment(db: Session, customer_number: int, check_number: str):
    db_payment = db.query(models.Payment).filter(
        models.Payment.customerNumber == customer_number,
        models.Payment.checkNumber == check_number
    ).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment record not found")
    return db_payment

def get_payments_by_customer(db: Session, customer_number: int):
    return db.query(models.Payment).filter(models.Payment.customerNumber == customer_number).all()

def create_payment(db: Session, data: schemas.payment_schemas.PaymentCreate):
    db_payment = models.Payment(**data.model_dump())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def update_payment(db: Session, customer_number: int, check_number: str, data: schemas.payment_schemas.PaymentUpdate):
    db_payment = get_payment(db, customer_number, check_number)
    update_dict = data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_payment, key, value)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def delete_payment(db: Session, customer_number: int, check_number: str):
    db_payment = get_payment(db, customer_number, check_number)
    db.delete(db_payment)
    db.commit()
    return {"detail": "Payment record deleted"}