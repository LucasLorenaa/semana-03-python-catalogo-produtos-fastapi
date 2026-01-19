
from pydantic import BaseModel, Field, ConfigDict

class ProductBase(BaseModel):
    name: str = Field(..., max_length=120)
    sku: str = Field(..., max_length=50)
    price: float = Field(..., gt=0)
    active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = Field(None, max_length=120)
    sku: str | None = Field(None, max_length=50)
    price: float | None = Field(None, gt=0)
    active: bool | None = None

class Product(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

