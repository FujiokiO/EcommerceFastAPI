from typing import Optional

from sqlalchemy.orm import Session
from app.models import table_model, user_model


def create_address(db: Session, address_data: user_model.AddressCreate) -> table_model.Address:
    db_address = user_model.Address(**address_data.model_dump())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def get_address(db: Session, user_id: int) -> list[table_model.Address]:
    return db.query(table_model.Address).filter(table_model.Address.user_id == user_id).all()


def get_default_address(db: Session, user_id: int) -> Optional[table_model.Address]:
    return db.query(user_model.Address).filter(user_model.AddressBase.user_id == user_id,
                                               user_model.AddressBase.is_default == True).first()


def update_address(db: Session, address_id: int, address_data: user_model.AddressUpdate) -> table_model.Address:
    db_address = db.query(user_model.AddressBase).filter(user_model.AddressBase.id == address_id).first()
    db_address.update(address_data.model_dump())
    db.commit()
    return db_address


def update_default_address(db: Session, user_id: int, address_id: int) -> table_model.Address:
    # 先将其他地址的is_default字段置为False
    db.query(user_model.AddressBase).filter(user_model.AddressBase.user_id == user_id).update({user_model.AddressBase.is_default: False})
    # 再将指定的地址的is_default字段置为True
    db_address = db.query(user_model.AddressBase).filter(user_model.AddressBase.id == address_id).first()
    db_address.is_default = True
    db.commit()
    return db_address


def delete_address(db: Session, address_id: int) -> table_model.Address:
    db_address = db.query(table_model.Address).filter(user_model.AddressBase.id == address_id).first()
    db.delete(db_address)
    db.commit()
    return db_address
