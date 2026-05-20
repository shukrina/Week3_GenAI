from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..crud import payment_crud
from ..schemas import payment_schemas

router = APIRouter()

@router.get("/", response_model=List[payment_schemas.PaymentOut])
def read_payments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return payment_crud.get_payments(db, skip, limit)

@router.get("/{customerNumber}/{checkNumber}", response_model=payment_schemas.PaymentOut)
def read_payment(customerNumber: int, checkNumber: str, db: Session = Depends(get_db)):
    return payment_crud.get_payment(db, customerNumber, checkNumber)

@router.get("/customer/{customerNumber}", response_model=List[payment_schemas.PaymentOut])
def read_customer_payments(customerNumber: int, db: Session = Depends(get_db)):
    # Note: Returns [] if no payments found as per Page 18
    return payment_crud.get_payments_by_customer(db, customerNumber)

@router.post("/", response_model=payment_schemas.PaymentOut, status_code=status.HTTP_201_CREATED)
def create_payment(data: payment_schemas.PaymentCreate, db: Session = Depends(get_db)):
    return payment_crud.create_payment(db, data)

@router.put("/{customerNumber}/{checkNumber}", response_model=payment_schemas.PaymentOut)
def update_payment(customerNumber: int, checkNumber: str, data: payment_schemas.PaymentUpdate, db: Session = Depends(get_db)):
    return payment_crud.update_payment(db, customerNumber, checkNumber, data)

@router.delete("/{customerNumber}/{checkNumber}")
def delete_payment(customerNumber: int, checkNumber: str, db: Session = Depends(get_db)):
    return payment_crud.delete_payment(db, customerNumber, checkNumber)