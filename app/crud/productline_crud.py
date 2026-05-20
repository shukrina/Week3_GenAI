from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from .. import models
from ..schemas import productline_schemas
from ..logging_config import logger

def get_productlines(db: Session, skip: int = 0, limit: int = 10):
    logger.info("CRUD: Fetching all product lines")
    return db.query(models.ProductLine).offset(skip).limit(limit).all()

def get_productline(db: Session, product_line: str):
    db_line = db.query(models.ProductLine).filter(models.ProductLine.productLine == product_line).first()
    if not db_line:
        logger.warning(f"CRUD: ProductLine {product_line} not found")
        raise HTTPException(status_code=404, detail="Product line not found")
    return db_line

def create_productline(db: Session, line_data: productline_schemas.ProductLineCreate):
    db_line = models.ProductLine(**line_data.model_dump())
    db.add(db_line)
    db.commit()
    db.refresh(db_line)
    return db_line

def update_productline(db: Session, product_line: str, line_data: productline_schemas.ProductLineUpdate):
    db_line = get_productline(db, product_line)
    update_data = line_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_line, key, value)
    db.commit()
    db.refresh(db_line)
    return db_line

def delete_productline(db: Session, product_line: str):
    db_line = get_productline(db, product_line)
    try:
        db.delete(db_line)
        db.commit()
        logger.info(f"CRUD: Deleted product line {product_line}")
        return {"detail": "Product line deleted"}
    except IntegrityError:
        db.rollback()
        logger.error(f"CRUD: Conflict - Cannot delete {product_line} because it has products.")
        # Requirement Page 8: Return 409 Conflict
        raise HTTPException(
            status_code=409, 
            detail="Conflict: This product line cannot be deleted because it still contains products."
        )

def get_productline_with_products(db: Session, product_line: str):
    db_line = get_productline(db, product_line)
    return db_line