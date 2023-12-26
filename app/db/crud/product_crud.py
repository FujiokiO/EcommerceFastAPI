
from sqlalchemy.orm import Session

from app.models.table_model import GoodsInfo


def get_product_by_name(db: Session, name: str):
    return db.query(GoodsInfo).filter(GoodsInfo.name == name).first()


def get_product_by_id(db: Session, id: int):
    return db.query(GoodsInfo).filter(GoodsInfo.id == id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(GoodsInfo).offset(skip).limit(limit).all()


def create_product(db: Session, product: GoodsInfo):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
