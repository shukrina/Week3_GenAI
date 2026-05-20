from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..crud import office_crud
from ..schemas import office_schemas

router = APIRouter()

@router.get("/", response_model=List[office_schemas.OfficeOut])
def read_offices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return office_crud.get_offices(db, skip=skip, limit=limit)

@router.get("/{officeCode}", response_model=office_schemas.OfficeOut)
def read_office(officeCode: str, db: Session = Depends(get_db)):
    return office_crud.get_office(db, officeCode)

@router.get("/{officeCode}/employees")
def read_office_employees(officeCode: str, db: Session = Depends(get_db)):
    office = office_crud.get_office_with_employees(db, officeCode)
    # Returns [] if no employees, as per Page 10 notes
    return office.employees

@router.post("/", response_model=office_schemas.OfficeOut, status_code=status.HTTP_201_CREATED)
def create_office(office: office_schemas.OfficeCreate, db: Session = Depends(get_db)):
    return office_crud.create_office(db, office)

@router.put("/{officeCode}", response_model=office_schemas.OfficeOut)
def update_office(officeCode: str, office_data: office_schemas.OfficeUpdate, db: Session = Depends(get_db)):
    return office_crud.update_office(db, officeCode, office_data)

@router.delete("/{officeCode}")
def delete_office(officeCode: str, db: Session = Depends(get_db)):
    return office_crud.delete_office(db, officeCode)