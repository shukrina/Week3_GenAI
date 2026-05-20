from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from .. import models
from ..schemas import office_schemas
from ..logging_config import logger

def get_offices(db: Session, skip: int = 0, limit: int = 10):
    logger.info(f"CRUD: Fetching offices skip={skip}, limit={limit}")
    return db.query(models.Office).offset(skip).limit(limit).all()

def get_office(db: Session, office_code: str):
    db_office = db.query(models.Office).filter(models.Office.officeCode == office_code).first()
    if not db_office:
        logger.warning(f"CRUD: Office {office_code} not found")
        raise HTTPException(status_code=404, detail="Office not found")
    return db_office

def create_office(db: Session, office_data: office_schemas.OfficeCreate):
    logger.info(f"CRUD: Creating office {office_data.officeCode}")
    db_office = models.Office(**office_data.model_dump())
    db.add(db_office)
    try:
        db.commit()
        db.refresh(db_office)
        return db_office
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=422, detail="Office code already exists or invalid data.")

def update_office(db: Session, office_code: str, office_data: office_schemas.OfficeUpdate):
    db_office = get_office(db, office_code)
    update_dict = office_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_office, key, value)
    db.commit()
    db.refresh(db_office)
    return db_office

def delete_office(db: Session, office_code: str):
    db_office = get_office(db, office_code)
    try:
        db.delete(db_office)
        db.commit()
        return {"detail": f"Office {office_code} deleted successfully"}
    except IntegrityError:
        db.rollback()
        logger.error(f"CRUD: Cannot delete office {office_code} - Employees assigned here.")
        # Requirement Page 10: Return 409
        raise HTTPException(status_code=409, detail="Cannot delete office; employees are still assigned to it.")

def get_office_with_employees(db: Session, office_code: str):
    return get_office(db, office_code)