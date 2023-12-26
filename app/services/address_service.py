from sqlalchemy.orm import Session
from app.db.crud import address_crud
from app.models import user_model


def create_address(db: Session, address_data: user_model.AddressCreate):
    return address_crud.create_address(db, address_data)


def update_address(db: Session, address_id: int, address_data: user_model.AddressCreate):
    return address_crud.update_address(db, address_id, address_data)


def delete_address(db: Session, address_id: int):
    return address_crud.delete_address(db, address_id)


def get_addresses(db: Session, user_id: int):
    return address_crud.get_address(db, user_id)


def get_addresses_by_user_id(db: Session, user_id: int):
    return address_crud.get_addresses_by_user_id(db, user_id)


def get_address(db: Session, address_id: int):
    return address_crud.get_address(db, address_id)


def get_default_address(db: Session, user_id: int, address_curd=None):
    return address_curd.get_default_address(db, user_id)
