# db/crud/

from sqlalchemy.orm import Session
from app.models.user_model import OrderStatus
from app.models import table_model


def update_order_status(db: Session, order_id: int, new_status: OrderStatus):
    # 在数据库中更新订单状态
    db_order = db.query(table_model).filter(table_model.id == order_id).first()

    if db_order:
        db_order.status = new_status
        db.commit()

    return db_order
