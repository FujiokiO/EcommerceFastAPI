"""用户模型"""
from typing import Union, Optional
from enum import Enum

from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    """用户基本信息"""
    username: str
    email: Union[EmailStr, None] = None
    is_disabled: Union[bool, None] = False
    is_admin: Union[bool, None] = False


class RegisterUser(BaseUser):
    verification_code: str
    password: str
    hashed_password: Union[str, None] = None


class UserInDB(BaseUser):
    """表示数据库中实际存储的用户模型"""
    id: int
    hashed_password: Union[str, None] = None


# *********************************用户地址模型********************************************
class AddressBase(BaseModel):
    user_id: int
    province: str
    city: str
    district: str
    street: str
    postal_code: str
    detail: str
    is_default: bool


"""
这样的Pydantic模型可以用于API端点的请求和响应验证。
在路由处理函数中，你可以使用AddressCreate来验证创建请求，
AddressUpdate来验证更新请求，而Address则可以用于返回。
"""


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class Address(AddressBase):
    id: int
    user_id: int
    is_default: Optional[bool]

    class Config:
        from_attributes = True


# *******************************订单状态及相关模型********************************************
class OrderStatus(Enum):
    """
    订单状态
    """
    PENDING_PAYMENT = "待支付"
    PROCESSING = "处理中"
    PAID = "已支付"
    PACKING = "已发货"
    IN_TRANSIT = "运输中"
    SHIPPED = "已收货"
    DELIVERED = "已交付"
    COMPLITED = "已完成"
    CANCELED = "已取消"
    RETURNED = "已退货"
    REFUNDED = "已退款"
    REFUND_FAILED = "退款失败"
    REFUND_SUCCESS = "退款成功"
    REFUND_PENDING = "退款中"
    REFUND_REJECTED = "退款被拒绝"
    REFUND_CANCELED = "退款取消"

    @classmethod
    def is_valid_status(cls, status):
        # 判断状态是否有效
        # 此方法返回一个布尔值，表示传入的状态是否存在于'OrderStatus'类的字典中
        return status in cls.__dict__.values()


class Order(BaseModel):
    id: int  # 订单id
    user_id: int  # 与订单关联的用户id
    product_id: int  # 与订单关联的产品id
    quantity: int  # 订单关联的产品数量
    status: OrderStatus  # 订单状态
    created_at: str  # 订单创建时间
    updated_at: str  # 订单更新时间

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    user_id: int  # 订单关联的用户id
    product_id: int  # 订单关联的产品id
    quantity: int  # 订单关联的产品数量
    status: OrderStatus  # 订单状态

    class Config:
        from_attributes = True


class OrderUpdate(BaseModel):
    status: OrderStatus  # 订单状态

    class Config:
        from_attributes = True


class OrderInDB(Order):
    id: int  # 订单id
    user_id: int  # 订单关联的用户id
    product_id: int  # 订单关联的产品id
    quantity: int  # 订单关联的产品数量
    status: OrderStatus  # 订单状态
    created_at: str  # 订单创建时间
    updated_at: str  # 订单更新时间

    class Config:
        from_attributes = True


class OrderInResponse(Order):
    id: int  # 订单id
    user_id: int  # 订单关联的用户id
    product_id: int  # 订单关联的产品id
    quantity: int  # 订单关联产品数量
    status: OrderStatus  # 订单状态
    created_at: str  # 订单创建时间
    updated_at: str  # 订单更新时间

    class Config:
        from_attributes = True


#   ****************************商品信息模型******************************


"""
# 用户个人资料模型
class UserProfile(BaseModel):
    full_name: str
    date_of_birth: str  # 可以使用 datetime 类型
    phone_number: Optional[str] = None
    addresses: List[Address] = []


# 用户认证信息模型
class UserAuth(BaseModel):
    username: str
    email: str
    hashed_password: str


# 用户订单历史模型
class OrderHistory(BaseModel):
    order_id: str
    total_amount: float
    items: List[str]
    # 其他订单相关信息


# 全面的用户类，包含个人资料、认证信息和订单历史
class User(BaseModel):
    profile: UserProfile
    auth: UserAuth
    order_history: List[OrderHistory] = []
"""
