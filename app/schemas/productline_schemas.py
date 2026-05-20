from pydantic import BaseModel
from typing import Optional
from .product_schemas import ProductOut
from typing import List

class ProductLineBase(BaseModel):
    productLine: str
    textDescription: Optional[str] = None
    htmlDescription: Optional[str] = None
    # Note: image is binary data (bytes)
    image: Optional[bytes] = None

class ProductLineCreate(ProductLineBase):
    pass

class ProductLineUpdate(BaseModel):
    textDescription: Optional[str] = None
    htmlDescription: Optional[str] = None
    image: Optional[bytes] = None

class ProductLineOut(ProductLineBase):
    # Optional: We can choose to exclude image from default output 
    # if it's too large for a standard list view.
    class Config:
        from_attributes = True

class ProductLineWithProducts(ProductLineOut):
    products: List[ProductOut] = []