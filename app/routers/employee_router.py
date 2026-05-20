from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..crud import employee_crud
from ..schemas import employee_schemas

router = APIRouter()

@router.get("/", response_model=List[employee_schemas.EmployeeOut])
def read_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return employee_crud.get_employees(db, skip=skip, limit=limit)

@router.get("/{employeeNumber}", response_model=employee_schemas.EmployeeOut)
def read_employee(employeeNumber: int, db: Session = Depends(get_db)):
    return employee_crud.get_employee(db, employeeNumber)

@router.get("/{employeeNumber}/customers")
def read_employee_customers(employeeNumber: int, db: Session = Depends(get_db)):
    customers = employee_crud.get_employee_customers(db, employeeNumber)
    return customers # Returns [] if none found

@router.get("/{employeeNumber}/reports", response_model=List[employee_schemas.EmployeeOut])
def read_employee_reports(employeeNumber: int, db: Session = Depends(get_db)):
    return employee_crud.get_employee_reports(db, employeeNumber)

@router.post("/", response_model=employee_schemas.EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(emp: employee_schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return employee_crud.create_employee(db, emp)

@router.put("/{employeeNumber}", response_model=employee_schemas.EmployeeOut)
def update_employee(employeeNumber: int, emp_data: employee_schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    return employee_crud.update_employee(db, employeeNumber, emp_data)

@router.delete("/{employeeNumber}")
def delete_employee(employeeNumber: int, db: Session = Depends(get_db)):
    return employee_crud.delete_employee(db, employeeNumber)