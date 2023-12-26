from typing import Optional, List
from pydantic import BaseModel, Field


class Basic_GoodsInfo(BaseModel):
    id: int
    name: str
    amount: int
    unit_price: float
    variety: str
    color: str
    occasion: str
    description: str
    image: str


# class Updated_GoodsInfo(BaseModel):
#     id: int
#     name: Optional[str] = None
#     amount: Optional[int] = None
#     unit_price: Optional[float] = None
#     variety: Optional[str] = None
#     color: Optional[str] = None
#     occasion: Optional[str] = None
#     description: Optional[str] = None
#     image: Optional[str] = None


# 管理员增
class CreateGoods(BaseModel):
    id: int = Field(..., title="ID", description="商品ID")
    name: str = Field(..., title="Name", description="商品名称")
    amount: int = Field(..., title="Amount", description="数量")
    unit_price: float = Field(..., title="Unit Price", description="单价")
    variety: str = Field(..., title="Variety", description="品种")
    color: str = Field(..., title="Color", description="花色")
    occasion: str = Field(..., title="Occasion", description="使用场合")
    description: str = Field(..., title="Description", description="商品描述")
    image: str = Field(..., title="Image", description="图片")


# 管理员改
class UpdateGoods(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    amount: Optional[int] = None
    unit_price: Optional[float] = None
    variety: Optional[str] = None
    color: Optional[str] = None
    occasion: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None


