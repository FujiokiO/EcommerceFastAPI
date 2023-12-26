from dataclasses import asdict
from sqlalchemy import text
from sqlalchemy.engine.row import RowProxy
from sqlalchemy.orm import Session
from app.models.goods_model import Basic_GoodsInfo, CreateGoods, UpdateGoods
from typing import Union, List

from app.models.table_model import GoodsInfo


#创建商品并添加到数据库
def create_goods(db: Session, new_goods: CreateGoods, goods_id: int = None) -> Basic_GoodsInfo:
    insert_query = text("""
        INSERT INTO goods_info (id, name, amount, unit_price, variety, color, occasion, description, image) 
        VALUES (:id, :name, :amount, :unit_price, :variety, :color, :occasion, :description, :image)
        RETURNING id, name, amount, unit_price, variety, color, occasion, description, image
    """)

    result = db.execute(insert_query, {
        'id': goods_id,
        'name': new_goods.name,
        'amount': new_goods.amount,
        'unit_price': new_goods.unit_price,
        'variety': new_goods.variety,
        'color': new_goods.color,
        'occasion': new_goods.occasion,
        'description': new_goods.description,
        'image': new_goods.image
    }).fetchone()

    db.commit()

    if isinstance(result, RowProxy):
        result_dict = result._asdict()
        return Basic_GoodsInfo(**result_dict)
#_asdict() 是 SQLAlchemy 中 RowProxy 对象的方法，它返回一个字典，其中键是列名，值是相应的列值。
# 这个方法是 SQLAlchemy 提供的特定于其结果代理对象的功能。



    # 处理其他情况或者返回默认值，根据你的业务需求
    return None


def get_update_goods(db: Session, partial_id: int) :
    query = text("SELECT * FROM goods_info WHERE CAST(id AS TEXT) LIKE :partial_id")
    goods_rows = db.execute(query, {"partial_id": f"%{partial_id}%"}).fetchall()

    print("goods_rows:", goods_rows)  # Add this line

    # 确保查询结果是一个字典的列表，而不是元组的列表
    basic_goods_list = [UpdateGoods(
        id=row[0],  # 假设ID是第一个元素，根据实际情况修改
        name=row[1],  # 同样地，根据实际情况调整索引
        amount=row[2],
        unit_price=row[3],
        variety=row[4],
        color=row[5],
        occasion=row[6],
        description=row[7],
        image=row[8]
    ) for row in goods_rows]

    return basic_goods_list


#从数据库中获取特定商品的信息
def get_goods(db: Session, partial_id: int) :
    query = text("SELECT * FROM goods_info WHERE CAST(id AS TEXT) LIKE :partial_id")
    goods_rows = db.execute(query, {"partial_id": f"%{partial_id}%"}).fetchall()

    print("goods_rows:", goods_rows)  # Add this line

    # 确保查询结果是一个字典的列表，而不是元组的列表
    basic_goods_list = [Basic_GoodsInfo(
        id=row[0],  # 假设ID是第一个元素，根据实际情况修改
        name=row[1],  # 同样地，根据实际情况调整索引
        amount=row[2],
        unit_price=row[3],
        variety=row[4],
        color=row[5],
        occasion=row[6],
        description=row[7],
        image=row[8]
    ) for row in goods_rows]

    return basic_goods_list
#.fetchone() 方法用于从结果集中提取一行数据。如果查询没有匹配的行，则返回 None
#execute:Session 对象的一个基本方法，用于执行 SQL 查询或命令。


#从数据库中获取所有商品的信息
def get_all_goods(db: Session) -> List[Basic_GoodsInfo]:
    query = text("SELECT * FROM goods_info")
    goods_rows = db.execute(query).fetchall()

    # 使用解包方式将查询结果映射为 Basic_GoodsInfo 类型的列表
    basic_goods_list = [Basic_GoodsInfo(**dict(row)) for row in goods_rows]

    return basic_goods_list

#更新特定商品的信息
from sqlalchemy.orm import Query


# def update_goods(db: Session, goods_id: int, updated_info: UpdateGoods):
#     # 获取当前商品的信息
#     existing_goods = get_goods(db, goods_id)
#     if not existing_goods:
#         return None  # 商品不存在，可以根据实际需求进行处理
#
#     # 使用 SQLAlchemy Query 对象进行更新
#     db.query(GoodsInfo).filter(GoodsInfo.id == goods_id).update({
#         'name': updated_info.name,
#         'amount': updated_info.amount,
#         'unit_price': updated_info.unit_price,
#         'variety': updated_info.variety,
#         'color': updated_info.color,
#         'occasion': updated_info.occasion,
#         'description': updated_info.description,
#         'image': updated_info.image,
#     })
#
#     # 提交更改到数据库
#     db.commit()
#
#     # 再次查询数据库获取最新的商品信息
#     updated_goods = get_goods(db, goods_id)
#
#     # 返回更新后的商品信息
#     return updated_goods[0] if updated_goods else None



#从数据库中删除特定商品
def delete_goods(db: Session, goods_id: int) -> Union[Basic_GoodsInfo, None]:
    delete_query = text("DELETE FROM goods_info WHERE id=:goods_id RETURNING *")
    deleted_goods = db.execute(delete_query, {"goods_id": goods_id}).fetchone()

    if not deleted_goods:
        return None  # 商品不存在，可以根据实际需求进行处理

    # 提交更改到数据库
    db.commit()

    # 使用 _asdict() 方法将 RowProxy 转换为字典
    deleted_goods_dict = deleted_goods._asdict()

    return Basic_GoodsInfo(
        id=deleted_goods_dict['id'],
        name=deleted_goods_dict['name'],
        amount=deleted_goods_dict['amount'],
        unit_price=deleted_goods_dict['unit_price'],
        variety=deleted_goods_dict['variety'],
        color=deleted_goods_dict['color'],
        occasion=deleted_goods_dict['occasion'],
        description=deleted_goods_dict['description'],
        image=deleted_goods_dict['image']
    )



