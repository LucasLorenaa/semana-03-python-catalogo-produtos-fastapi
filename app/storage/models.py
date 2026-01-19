
from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    price = Column(Float, nullable=False)
    active = Column(Boolean, default=True)

