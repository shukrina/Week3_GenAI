from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..crud import productline_crud
from ..schemas import productline_schemas

router = APIRouter()

@router.get("/", response_model=List[productline_schemas.ProductLineOut])
def read_productlines(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return productline_crud.get_productlines(db, skip=skip, limit=limit)

@router.get("/{productLine}", response_model=productline_schemas.ProductLineOut)
def read_productline(productLine: str, db: Session = Depends(get_db)):
    return productline_crud.get_productline(db, productLine)

@router.get("/{productLine}/products", response_model=productline_schemas.ProductLineWithProducts)
def read_productline_products(productLine: str, db: Session = Depends(get_db)):
    return productline_crud.get_productline_with_products(db, productLine)

@router.post("/", response_model=productline_schemas.ProductLineOut, status_code=status.HTTP_201_CREATED)
def create_productline(line: productline_schemas.ProductLineCreate, db: Session = Depends(get_db)):
    return productline_crud.create_productline(db, line)

@router.put("/{productLine}", response_model=productline_schemas.ProductLineOut)
def update_productline(productLine: str, line_data: productline_schemas.ProductLineUpdate, db: Session = Depends(get_db)):
    return productline_crud.update_productline(db, productLine, line_data)

@router.delete("/{productLine}")
def delete_productline(productLine: str, db: Session = Depends(get_db)):
    return productline_crud.delete_productline(db, productLine)