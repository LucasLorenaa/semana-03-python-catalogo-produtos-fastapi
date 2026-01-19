
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ...storage import crud, models
from .. import schemas
from ...storage.database import SessionLocal

router = APIRouter(prefix="/products", tags=["products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_product(db, product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="SKU already exists")

@router.get("/")
def list_products(skip: int = 0, limit: int = 10, min_price: float | None = None, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit, min_price=min_price)
    total = db.query(models.Product).count()
    return {
        "items": products,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, updates: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.update_product(db, db_product, updates)

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    crud.delete_product(db, db_product)
    return {"detail": "Product deleted"}

