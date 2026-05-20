from pydantic import BaseModel, Field, field_validator
from typing import Optional
from decimal import Decimal
from datetime import date

class PaymentBase(BaseModel):
    paymentDate: date
    amount: Decimal = Field(..., gt=0)

    @field_validator('paymentDate')
    @classmethod
    def date_not_in_future(cls, v):
        if v > date.today():
            raise ValueError('Payment date cannot be in the future')
        return v

class PaymentCreate(PaymentBase):
    customerNumber: int
    checkNumber: str

class PaymentUpdate(BaseModel):
    paymentDate: Optional[date] = None
    amount: Optional[Decimal] = Field(None, gt=0)

class PaymentOut(PaymentBase):
    customerNumber: int
    checkNumber: str
    class Config:
        from_attributes = True