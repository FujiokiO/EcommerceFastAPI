from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.base import get_db
from app.models import table_model,goods_model

router = APIRouter()

#这个应该是不对！！！！！！！！

# CRUD operation to get goods information based on various parameters
# @router.get("/search_goods", tags=["用户搜索模块"], response_model=List[goods_model.client_ReadGoods])
# async def get_goods_info(
#     occasion: Optional[str] = None,
#     variety: Optional[str] = None,
#     color: Optional[str] = None,
#     pattern: Optional[str] = '',
#     db: Session = Depends(get_db)
# ):
#     query = db.query(table_model.GoodsInfo)
#
#     # Filtering based on parameters
#     if occasion:
#         query = query.filter(table_model.GoodsInfo.occasion == occasion)
#     if variety:
#         query = query.filter(table_model.GoodsInfo.variety == variety)
#     if color:
#         query = query.filter(table_model.GoodsInfo.color == color)
#
#     # Dynamically add pattern filter based on include_pattern
#     if pattern:
#         query = query.filter(or_(
#             table_model.GoodsInfo.occasion.like(f'%{pattern}%'),
#             table_model.GoodsInfo.variety.like(f'%{pattern}%'),
#             table_model.GoodsInfo.color.like(f'%{pattern}%')
#         ))
#
#     goods = query.all()
#     return goods
