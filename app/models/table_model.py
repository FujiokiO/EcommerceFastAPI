from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, comment='用户ID')
    username = Column(String(50), unique=True, nullable=False, comment='用户名')
    email = Column(String(100), unique=True, nullable=False, comment='邮箱')
    password = Column(String(100), nullable=False, comment='密码')
    is_admin = Column(Boolean, default=False, comment='是否管理员')
    is_disabled = Column(Boolean, default=False, comment='是否禁用')
    registration_time = Column(DateTime, default=func.now(), comment='注册时间')
    last_login_time = Column(DateTime, comment='最后登录时间')

    addresses = relationship("Address", back_populates="user")
    orders = relationship('Order', back_populates='user')
    carts = relationship('Cart', back_populates='user')


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, comment='地址ID')
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, comment='用户ID')
    country = Column(String(100), comment='国家')
    province_or_state = Column(String(100), comment='省份/州')
    city = Column(String(100), comment='城市')
    street = Column(String(255), comment='街道')
    postal_code = Column(String(20), comment='邮政编码')
    is_default = Column(Boolean, default=False, comment='是否默认')

    user = relationship("User", back_populates="addresses")
    orders = relationship('Order', back_populates='address')


class VerificationCode(Base):
    __tablename__ = 'verification_code'
    id = Column(Integer, primary_key=True, index=True, comment='验证码ID')
    email = Column(String(100), unique=True, nullable=False, comment='邮箱')
    code = Column(String(10), nullable=False, comment='验证码')
    created_at = Column(DateTime, default=func.now(), nullable=False, comment='创建时间')
    expiration_time = Column(DateTime, nullable=False, comment='过期时间')
    is_used = Column(Boolean, default=False, comment='是否已使用')


class Token(Base):
    __tablename__ = 'token'
    type = Column(String, primary_key=True, index=True, comment='令牌类型')
    content = Column(JSON, comment='令牌内容')


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, comment='订单ID')
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, comment='用户ID')
    total_price = Column(Float, nullable=False, comment='总价')
    address_id = Column(Integer, ForeignKey('address.id'), nullable=False, comment='地址ID')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    order_status = Column(Integer, default=0, nullable=False, comment='订单状态')
    processed_at = Column(DateTime, nullable=True, comment='处理时间')

    user = relationship('User', back_populates='orders')
    address = relationship('Address', back_populates='orders')
    order_detail = relationship('OrderDetail', back_populates='order')


class OrderDetail(Base):
    __tablename__ = 'order_detail'
    id = Column(Integer, primary_key=True, comment='订单详情ID')
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False, comment='订单ID')
    goods_id = Column(Integer, ForeignKey('goods_info.id'), nullable=False, comment='商品ID')
    unit_price = Column(Float, nullable=False, comment='单价')
    quantity = Column(Integer, nullable=False, comment='数量')

    order = relationship('Order', back_populates='order_detail')
    goods = relationship('GoodsInfo', back_populates='order_detail')


class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='购物车ID')
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, comment='用户ID')
    goods_id = Column(Integer, ForeignKey('goods_info.id'), nullable=False, comment='商品ID')
    amount = Column(Integer, nullable=False, comment='商品数量')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    goods = relationship('GoodsInfo', back_populates='carts')
    user = relationship('User', back_populates='carts')


class GoodsInfo(Base):
    __tablename__ = 'goods_info'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='商品ID')
    name = Column(String(50), nullable=True, comment='商品名称')
    amount = Column(Integer, nullable=True, comment='数量')
    unit_price = Column(Float, nullable=True, comment='单价')
    variety = Column(String(50), comment='品种')
    color = Column(String(50), comment='花色')
    occasion = Column(String(50), nullable=True, comment='使用场合')
    description=Column(Text,nullable=True,comment='商品描述')
    image = Column(String, comment='图片')

    carts = relationship('Cart', back_populates='goods')
    order_detail = relationship('OrderDetail', back_populates='goods')
