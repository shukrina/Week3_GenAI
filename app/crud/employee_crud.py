from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from .. import models
from ..schemas import employee_schemas
from ..logging_config import logger

def get_employees(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Employee).offset(skip).limit(limit).all()

def get_employee(db: Session, emp_id: int):
    db_emp = db.query(models.Employee).filter(models.Employee.employeeNumber == emp_id).first()
    if not db_emp:
        logger.warning(f"CRUD: Employee {emp_id} not found")
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_emp

def create_employee(db: Session, emp_data: employee_schemas.EmployeeCreate):
    db_emp = models.Employee(**emp_data.model_dump())
    db.add(db_emp)
    try:
        db.commit()
        db.refresh(db_emp)
        return db_emp
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=422, detail="Constraint violation: Check officeCode or reportsTo IDs.")

def update_employee(db: Session, emp_id: int, emp_data: employee_schemas.EmployeeUpdate):
    db_emp = get_employee(db, emp_id)
    update_dict = emp_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_emp, key, value)
    db.commit()
    db.refresh(db_emp)
    return db_emp

def delete_employee(db: Session, emp_id: int):
    db_emp = get_employee(db, emp_id)
    try:
        db.delete(db_emp)
        db.commit()
        return {"detail": "Employee deleted"}
    except IntegrityError:
        db.rollback()
        # Requirement Page 12: Return 409 if they have reports or customers
        raise HTTPException(
            status_code=409, 
            detail="Cannot delete employee; they have direct reports or are assigned to customers."
        )

# Get all employees who report to this manager
def get_employee_reports(db: Session, emp_id: int):
    get_employee(db, emp_id) # Verify existence
    return db.query(models.Employee).filter(models.Employee.reportsTo == emp_id).all()

# Get all customers managed by this employee
def get_employee_customers(db: Session, emp_id: int):
    db_emp = get_employee(db, emp_id)
    return db_emp.customers