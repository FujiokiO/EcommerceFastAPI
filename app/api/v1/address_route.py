from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import base
from app.services import address_service
from app.models import user_model

router = APIRouter()


@router.post("/address", tags=["收货地址模块"])
# 新建地址函数
def create_address(
        address_data: user_model.AddressCreate,
        db: Session = Depends(base.SessionLocal),
        current_user=user_model.BaseUser
):
    return address_service.create_address(address_data, db, current_user)


@router.put("/address", tags=["收货地址模块"])
def update_address(
        address_data: user_model.AddressUpdate,
        update=user_model.AddressUpdate,
        current_user=user_model.BaseUser
):
    return address_service.update_address(address_data, update, current_user)


@router.delete("/address/delete", tags=["收货地址模块"])
def delete_address(
        address_id: int,
        db: Session = Depends(base.SessionLocal),
        current_user=user_model.BaseUser
):
    return address_service.delete_address(address_id, db, current_user.id)


@router.get("/address", tags=["收货地址模块"])
def get_addresses(
        db: Session = Depends(base.SessionLocal),
        current_user=user_model.BaseUser
):
    return address_service.get_address(db, current_user.id)


@router.get("/address/default", tags=["收货地址模块"])
def get_default_address(
        db: Session = Depends(base.SessionLocal),
        current_user=user_model.BaseUser
):
    return address_service.get_default_address(db, current_user.id)
