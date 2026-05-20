from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

# Import our layers
from ..database import get_db
from ..crud import product_crud
from ..schemas import product_schemas
from ..logging_config import logger

router = APIRouter()

# 1. GET /products - List all products with pagination
@router.get("/", response_model=List[product_schemas.ProductOut])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info(f"ROUTER: Incoming request GET /products?skip={skip}&limit={limit}")
    products = product_crud.get_products(db, skip=skip, limit=limit)
    logger.info(f"ROUTER: Returning {len(products)} products with status 200")
    return products

# 2. GET /products/{productCode} - Get single product
@router.get("/{productCode}", response_model=product_schemas.ProductOut)
def read_product(productCode: str, db: Session = Depends(get_db)):
    logger.info(f"ROUTER: Incoming request GET /products/{productCode}")
    product = product_crud.get_product(db, productCode)
    logger.info(f"ROUTER: Product {productCode} found and returned")
    return product

# 3. GET /products/{productCode}/orderdetails - Get product with line items
@router.get("/{productCode}/orderdetails")
def read_product_order_details(productCode: str, db: Session = Depends(get_db)):
    logger.info(f"ROUTER: Incoming request GET /products/{productCode}/orderdetails")
    product = product_crud.get_product_with_orderdetails(db, productCode)
    
    # PDF Requirement: Return empty list [] if no orders exist. 
    # SQLAlchemy relationship returns an empty list by default if no related records exist.
    logger.info(f"ROUTER: Returning order details for product {productCode}")
    return product.order_details

# 4. POST /products - Create a new product
@router.post("/", response_model=product_schemas.ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product: product_schemas.ProductCreate, db: Session = Depends(get_db)):
    logger.info(f"ROUTER: Incoming request POST /products - Data: {product.productCode}")
    new_product = product_crud.create_product(db, product)
    logger.info(f"ROUTER: Successfully created product {new_product.productCode}")
    return new_product

# 5. PUT /products/{productCode} - Update a product (Partial)
@router.put("/{productCode}", response_model=product_schemas.ProductOut)
def update_product(productCode: str, product_data: product_schemas.ProductUpdate, db: Session = Depends(get_db)):
    logger.info(f"ROUTER: Incoming request PUT /products/{productCode}")
    updated_product = product_crud.update_product(db, productCode, product_data)
    logger.info(f"ROUTER: Successfully updated product {productCode}")
    return updated_product

# 6. DELETE /products/{productCode} - Delete a product
@router.delete("/{productCode}")
def delete_product(productCode: str, db: Session = Depends(get_db)):
    logger.info(f"ROUTER: Incoming request DELETE /products/{productCode}")
    result = product_crud.delete_product(db, productCode)
    logger.info(f"ROUTER: Product {productCode} deleted successfully")
    return result