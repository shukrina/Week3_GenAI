from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class ProductBase(BaseModel):
    productName: str
    productLine: str
    productScale: str
    productVendor: str
    productDescription: str
    quantityInStock: int = Field(..., ge=0)
    buyPrice: Decimal
    MSRP: Decimal

class ProductCreate(ProductBase):
    productCode: str  # Client provided PK

class ProductUpdate(BaseModel):
    productName: Optional[str] = None
    productLine: Optional[str] = None
    quantityInStock: Optional[int] = None
    buyPrice: Optional[Decimal] = None
    MSRP: Optional[Decimal] = None

class ProductOut(ProductBase):
    productCode: str
    class Config:
        from_attributes = True