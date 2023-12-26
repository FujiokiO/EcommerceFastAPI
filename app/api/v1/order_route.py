import datetime

from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from app.models.user_model import OrderStatus
from app.services import auth_service
from app.models import user_model, table_model

router = APIRouter()


# 共享的身份验证函数
def get_current_user(token: str = Depends(auth_service.oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth_service.SECRET_KEY, algorithms=[auth_service.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    if username not in user_model.BaseUser.username:
        raise credentials_exception
    return user_model.BaseUser.username


@router.put("/orders/{order_id}/update_status", tags=["订单模块"])
def update_order_status(order_id: int, order_update: OrderStatus, current_user: dict = Depends(get_current_user)):
    # 在这里执行更新订单状态的逻辑
    # ...
    # 检查用户权限
    if current_user.get("diaabled"):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # 检查订单是否存在
    if order_id not in table_model.Order:
        raise HTTPException(status_code=404, detail="Order not found")

    # 检查新状态是否有效
    if not OrderStatus.is_valid_status(order_update):
        raise HTTPException(status_code=400, detail="Invalid status")

    # 更新订单状态
    table_model.Order[order_id].order_status = order_update
    table_model.Order[order_id].updated_at = datetime.datetime

    return {"message": "Order status updated successfully"}


@router.get("/orders/{order_id}/get_status", tags=["订单模块"])
def get_order_status(order_id: int, current_user: dict = Depends(get_current_user)):
    # 在这里执行获取订单状态的逻辑
    # ...
    # 检查用户权限检查用户权限
    if current_user.get("diaabled"):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # 检查订单是否存在
    if order_id not in table_model.Order:
        raise HTTPException(status_code=404, detail="Order not found")

    # 获取订单状态
    order_status = user_model.Order.Status
    return {"order_id": order_id, "status": order_status}
