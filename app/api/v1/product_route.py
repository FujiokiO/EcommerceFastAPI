
from fastapi import APIRouter, Query, HTTPException, Depends

from app.db.crud.product_crud import get_product_by_name

router = APIRouter()


@router.get("/products/", tags=["查询商品模块"])
def get_products(name: str = Query(regx=r'^[\u4e00-\u9fa5]+$')):
    """
   查询商品信息的接口

   Parameters:
       - name: 商品名称， 只包含中文字符


   Returns:
       - 商品信息
   """
    # 这里根据商品名称(name)进行查询， 并返回相应的结果
    # 可以调用数据库中的函数来获取商品信息
    product = get_product_by_name(name)

    if product is None:
        raise HTTPException(status_code=404, detail="商品不存在")

    return {"product_name": product.name, "price": product.price, "description": product.description}

    # 返回查询到的商品名称
