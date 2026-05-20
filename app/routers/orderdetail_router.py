from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..crud import orderdetail_crud
from ..schemas import orderdetail_schemas

router = APIRouter()

@router.get("/", response_model=List[orderdetail_schemas.OrderDetailOut])
def read_orderdetails(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return orderdetail_crud.get_orderdetails(db, skip, limit)

@router.get("/{orderNumber}/{productCode}", response_model=orderdetail_schemas.OrderDetailOut)
def read_orderdetail(orderNumber: int, productCode: str, db: Session = Depends(get_db)):
    return orderdetail_crud.get_orderdetail(db, orderNumber, productCode)

@router.get("/order/{orderNumber}", response_model=List[orderdetail_schemas.OrderDetailOut])
def read_by_order(orderNumber: int, db: Session = Depends(get_db)):
    return orderdetail_crud.get_details_by_order(db, orderNumber)

@router.get("/product/{productCode}", response_model=List[orderdetail_schemas.OrderDetailOut])
def read_by_product(productCode: str, db: Session = Depends(get_db)):
    return orderdetail_crud.get_details_by_product(db, productCode)

@router.post("/", response_model=orderdetail_schemas.OrderDetailOut, status_code=status.HTTP_201_CREATED)
def create_orderdetail(data: orderdetail_schemas.OrderDetailCreate, db: Session = Depends(get_db)):
    return orderdetail_crud.create_orderdetail(db, data)

@router.put("/{orderNumber}/{productCode}", response_model=orderdetail_schemas.OrderDetailOut)
def update_orderdetail(orderNumber: int, productCode: str, data: orderdetail_schemas.OrderDetailUpdate, db: Session = Depends(get_db)):
    return orderdetail_crud.update_orderdetail(db, orderNumber, productCode, data)

@router.delete("/{orderNumber}/{productCode}")
def delete_orderdetail(orderNumber: int, productCode: str, db: Session = Depends(get_db)):
    return orderdetail_crud.delete_orderdetail(db, orderNumber, productCode)