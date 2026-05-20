from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from .. import models
from ..schemas import product_schemas
from ..logging_config import logger

# 1. List all records with pagination
def get_products(db: Session, skip: int = 0, limit: int = 10):
    logger.info(f"CRUD: Fetching products - skip: {skip}, limit: {limit}")
    products = db.query(models.Product).offset(skip).limit(limit).all()
    logger.info(f"CRUD: Successfully retrieved {len(products)} products")
    return products

# 2. Get single record by primary key (productCode)
def get_product(db: Session, product_code: str):
    logger.info(f"CRUD: Fetching product with code: {product_code}")
    db_product = db.query(models.Product).filter(models.Product.productCode == product_code).first()
    
    if not db_product:
        logger.warning(f"CRUD: Product {product_code} not found")
        raise HTTPException(status_code=404, detail=f"Product with code {product_code} not found")
    
    return db_product

# 3. Insert a new record
def create_product(db: Session, product_data: product_schemas.ProductCreate):
    logger.info(f"CRUD: Creating new product: {product_data.productCode}")
    try:
        db_product = models.Product(**product_data.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        logger.info(f"CRUD: Successfully created product: {db_product.productCode}")
        return db_product
    except IntegrityError as e:
        db.rollback()
        logger.error(f"CRUD: Error creating product (FK or Duplicate): {str(e)}")
        # Requirement Page 5: Return 422 for FK constraint fails
        raise HTTPException(
            status_code=422, 
            detail="Invalid Foreign Key (productLine) or duplicate Product Code."
        )

# 4. Update an existing record (partial)
def update_product(db: Session, product_code: str, product_data: product_schemas.ProductUpdate):
    logger.info(f"CRUD: Updating product: {product_code}")
    db_product = get_product(db, product_code) # Reuses get_product for 404 check
    
    update_data = product_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    try:
        db.commit()
        db.refresh(db_product)
        logger.info(f"CRUD: Successfully updated product: {product_code}")
        return db_product
    except IntegrityError as e:
        db.rollback()
        logger.error(f"CRUD: Integrity error during update: {str(e)}")
        raise HTTPException(status_code=422, detail="Update failed due to constraint violation.")

# 5. Delete a record by primary key
def delete_product(db: Session, product_code: str):
    logger.info(f"CRUD: Deleting product: {product_code}")
    db_product = get_product(db, product_code) # Reuses get_product for 404 check
    
    try:
        db.delete(db_product)
        db.commit()
        logger.info(f"CRUD: Successfully deleted product: {product_code}")
        return {"detail": "Product deleted successfully"}
    except IntegrityError as e:
        db.rollback()
        logger.error(f"CRUD: Cannot delete product {product_code} (referenced by other tables)")
        raise HTTPException(status_code=409, detail="Cannot delete product; it is referenced in orders.")

# 6. Fetch record with related orderdetails
def get_product_with_orderdetails(db: Session, product_code: str):
    logger.info(f"CRUD: Fetching product {product_code} with order details")
    db_product = get_product(db, product_code)
    
    # SQLAlchemy relationship handles the join
    details = db_product.order_details
    logger.info(f"CRUD: Retrieved product {product_code} with {len(details)} line items")
    return db_product