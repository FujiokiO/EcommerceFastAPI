from typing import List, Union
from sqlalchemy.orm import Session
from app.db.crud.goods_crud import create_goods, delete_goods, get_goods, get_all_goods, get_update_goods
from app.models.goods_model import Basic_GoodsInfo, UpdateGoods, CreateGoods
from app.db.base import SessionLocal
from sqlalchemy import text

db = SessionLocal()


def create_new_goods(db: Session, new_goods: CreateGoods, goods_id: int = None) -> Basic_GoodsInfo:
    """从数据库中增加商品"""
    if goods_id is not None and (goods_id < 10000 or goods_id > 99999):
        raise ValueError("商品ID必须为5位长度")

    # 检查商品ID是否已存在
    existing_goods = get_goods(db, goods_id)
    if existing_goods:
        raise ValueError("商品ID已存在")

    try:
        return create_goods(db, new_goods, goods_id)
    except ValueError as ve:
        # 处理商品创建异常
        # 你可以选择将异常传递给调用者，或者在这里进行其他处理
        raise ve




def remove_goods(db: Session, goods_id: int) -> Union[Basic_GoodsInfo, None]:
    """从数据库中删除特定商品，并返回已删除的商品信息。"""
    deleted_goods = delete_goods(db=db, goods_id=goods_id)#这里卡我半天
    if not deleted_goods:
        raise ValueError("商品不存在，无法删除。")
    db.commit()
    # 返回已删除的商品信息，使用解包方式
    deleted_goods_info = Basic_GoodsInfo(**dict(deleted_goods))
    raise ValueError(f"商品删除成功，已删除的商品信息为: {deleted_goods_info}")


def get_goods_partial_id(partial_id: int) -> Basic_GoodsInfo:
    if partial_id > 99999:  # 判断是否大于5位数
        raise ValueError("ID不得大于5位")
    goods = get_goods(db=db, partial_id=partial_id)
    if goods:
        return goods
    else:
        raise ValueError("无相关商品")



from app.models.goods_model import UpdateGoods  # 请根据实际模块结构调整导入路径


def admin_update_goods(db: Session, goods_id: int, updated_info: dict) -> UpdateGoods:
    # 判断商品ID是否为5位长度
    if not (10000 <= goods_id <= 99999):
        raise ValueError("请输入5位长度ID")
    # 获取当前商品的信息
    existing_goods = get_goods(db, goods_id)

    # 处理可能返回的列表
    if isinstance(existing_goods, list):
        existing_goods = existing_goods[0] if existing_goods else None

    if not existing_goods:
        raise ValueError("商品不存在，请首先创建商品。")

    # 获取非空字段，如果值为 None 则不包含在更新中
    update_fields = {field: value for field, value in updated_info.items() if value is not None}

    # 如果没有提供要更新的字段，直接返回当前数据库中的商品信息
    if not update_fields:
        return UpdateGoods(**existing_goods.dict())  # 返回当前数据库中的商品信息

    # 使用合并运算符合并字典
    updated_data = {**existing_goods.dict(), **update_fields}

    # 构建 SQL UPDATE 语句
    update_sql = f"UPDATE goods_info SET {', '.join([f'{field} = :{field}' for field in update_fields.keys()])} WHERE id = :goods_id"

    # 执行 SQL UPDATE 语句
    db.execute(text(update_sql), {**update_fields, "goods_id": goods_id})

    # 提交更改到数据库
    db.commit()

    # 返回更新后的商品信息
    return UpdateGoods(**updated_data)









