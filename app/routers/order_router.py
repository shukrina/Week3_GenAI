from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..crud import order_crud
from ..schemas import order_schemas

router = APIRouter()

@router.get("/", response_model=List[order_schemas.OrderOut])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return order_crud.get_orders(db, skip=skip, limit=limit)

@router.get("/{orderNumber}", response_model=order_schemas.OrderOut)
def read_order(orderNumber: int, db: Session = Depends(get_db)):
    return order_crud.get_order(db, orderNumber)

@router.get("/{orderNumber}/orderdetails")
def read_order_details(orderNumber: int, db: Session = Depends(get_db)):
    order = order_crud.get_order(db, orderNumber)
    return order.details # Reuses relationship from models.py

@router.get("/customer/{customerNumber}", response_model=List[order_schemas.OrderOut])
def read_customer_orders(customerNumber: int, db: Session = Depends(get_db)):
    return order_crud.get_orders_by_customer(db, customerNumber)

@router.post("/", response_model=order_schemas.OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(order: order_schemas.OrderCreate, db: Session = Depends(get_db)):
    return order_crud.create_order(db, order)

@router.put("/{orderNumber}", response_model=order_schemas.OrderOut)
def update_order(orderNumber: int, order_data: order_schemas.OrderUpdate, db: Session = Depends(get_db)):
    return order_crud.update_order(db, orderNumber, order_data)

@router.delete("/{orderNumber}")
def delete_order(orderNumber: int, db: Session = Depends(get_db)):
    return order_crud.delete_order(db, orderNumber)