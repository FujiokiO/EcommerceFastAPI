"""add Tables as follow Order OrderDetai Cart and GoodsInfo

Revision ID: f4b8152a4bb2
Revises: da373f787d12
Create Date: 2023-12-24 15:03:02.511202

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from app.services.auth_service import get_password_hash

# revision identifiers, used by Alembic.
revision: str = 'f4b8152a4bb2'
down_revision: Union[str, None] = 'da373f787d12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('goods_info',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='商品ID'),
                    sa.Column('name', sa.String(length=50), nullable=False, comment='商品名称'),
                    sa.Column('amount', sa.Integer(), nullable=False, comment='数量'),
                    sa.Column('unit_price', sa.Float(), nullable=False, comment='单价'),
                    sa.Column('description', sa.Text(), nullable=True, comment='描述'),
                    sa.Column('image', sa.String(), nullable=True, comment='图片'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_index(op.f('ix_goods_info_id'), 'goods_info', ['id'], unique=False)
    op.create_table('token',
                    sa.Column('id', sa.Integer(), nullable=False, comment='令牌ID'),
                    sa.Column('access_token', sa.String(), nullable=True, comment='访问令牌'),
                    sa.Column('refresh_token', sa.String(), nullable=True, comment='刷新令牌'),
                    sa.Column('expires_at', sa.Integer(), nullable=True, comment='过期时间'),
                    sa.Column('is_expired', sa.Boolean(), nullable=True, comment='是否已过期'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_token_id'), 'token', ['id'], unique=False)
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False, comment='用户ID'),
                    sa.Column('username', sa.String(length=50), nullable=False, comment='用户名'),
                    sa.Column('email', sa.String(length=100), nullable=False, comment='邮箱'),
                    sa.Column('password', sa.String(length=100), nullable=False, comment='密码'),
                    sa.Column('is_admin', sa.Boolean(), nullable=True, comment='是否管理员'),
                    sa.Column('is_disabled', sa.Boolean(), nullable=True, comment='是否禁用'),
                    sa.Column('registration_time', sa.DateTime(), nullable=True, comment='注册时间'),
                    sa.Column('last_login_time', sa.DateTime(), nullable=True, comment='最后登录时间'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('username')
                    )
    op.create_table('verification_code',
                    sa.Column('id', sa.Integer(), nullable=False, comment='验证码ID'),
                    sa.Column('email', sa.String(length=100), nullable=False, comment='邮箱'),
                    sa.Column('code', sa.String(length=10), nullable=False, comment='验证码'),
                    sa.Column('created_at', sa.DateTime(), nullable=False, comment='创建时间'),
                    sa.Column('expiration_time', sa.DateTime(), nullable=False, comment='过期时间'),
                    sa.Column('is_used', sa.Boolean(), nullable=True, comment='是否已使用'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    op.create_index(op.f('ix_verification_code_id'), 'verification_code', ['id'], unique=False)
    op.create_table('address',
                    sa.Column('id', sa.Integer(), nullable=False, comment='地址ID'),
                    sa.Column('user_id', sa.Integer(), nullable=False, comment='用户ID'),
                    sa.Column('country', sa.String(length=100), nullable=True, comment='国家'),
                    sa.Column('province_or_state', sa.String(length=100), nullable=True, comment='省份/州'),
                    sa.Column('city', sa.String(length=100), nullable=True, comment='城市'),
                    sa.Column('street', sa.String(length=255), nullable=True, comment='街道'),
                    sa.Column('postal_code', sa.String(length=20), nullable=True, comment='邮政编码'),
                    sa.Column('is_default', sa.Boolean(), nullable=True, comment='是否默认'),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('cart',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='购物车ID'),
                    sa.Column('user_id', sa.Integer(), nullable=False, comment='用户ID'),
                    sa.Column('goods_id', sa.Integer(), nullable=False, comment='商品ID'),
                    sa.Column('amount', sa.Integer(), nullable=False, comment='商品数量'),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True,
                              comment='创建时间'),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True,
                              comment='更新时间'),
                    sa.ForeignKeyConstraint(['goods_id'], ['goods_info.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_cart_id'), 'cart', ['id'], unique=False)
    op.create_table('order',
                    sa.Column('id', sa.Integer(), nullable=False, comment='订单ID'),
                    sa.Column('user_id', sa.Integer(), nullable=False, comment='用户ID'),
                    sa.Column('total_price', sa.Float(), nullable=False, comment='总价'),
                    sa.Column('address_id', sa.Integer(), nullable=False, comment='地址ID'),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True,
                              comment='创建时间'),
                    sa.Column('order_status', sa.Integer(), nullable=False, comment='订单状态'),
                    sa.Column('processed_at', sa.DateTime(), nullable=True, comment='处理时间'),
                    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('order_detail',
                    sa.Column('id', sa.Integer(), nullable=False, comment='订单详情ID'),
                    sa.Column('order_id', sa.Integer(), nullable=False, comment='订单ID'),
                    sa.Column('goods_id', sa.Integer(), nullable=False, comment='商品ID'),
                    sa.Column('unit_price', sa.Float(), nullable=False, comment='单价'),
                    sa.Column('quantity', sa.Integer(), nullable=False, comment='数量'),
                    sa.ForeignKeyConstraint(['goods_id'], ['goods_info.id'], ),
                    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.drop_table('addresses')
    op.drop_table('users')
    op.drop_index('ix_verification_codes_id', table_name='verification_codes')
    op.drop_table('verification_codes')
    op.drop_index('ix_tokens_id', table_name='tokens')
    op.drop_table('tokens')
    # ### end Alembic commands ###
    admin_password_hash = get_password_hash("Pa$sW0rd")
    op.execute(
        f"""
        INSERT INTO "user" (username, email, password, is_admin, is_disabled, registration_time)
        VALUES ('admin', 'admin@dbcd.oky.wiki', '{admin_password_hash}', true, false, now())
        """
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tokens',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('access_token', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('refresh_token', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('expires_at', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('is_expired', sa.BOOLEAN(), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('id', name='tokens_pkey')
                    )
    op.create_index('ix_tokens_id', 'tokens', ['id'], unique=False)
    op.create_table('verification_codes',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
                    sa.Column('code', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
                    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
                    sa.Column('expiration_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
                    sa.Column('is_used', sa.BOOLEAN(), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('id', name='verification_codes_pkey'),
                    sa.UniqueConstraint('email', name='verification_codes_email_key')
                    )
    op.create_index('ix_verification_codes_id', 'verification_codes', ['id'], unique=False)
    op.create_table('users',
                    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"),
                              autoincrement=True, nullable=False),
                    sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
                    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
                    sa.Column('password', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
                    sa.Column('is_admin', sa.BOOLEAN(), autoincrement=False, nullable=True),
                    sa.Column('is_disabled', sa.BOOLEAN(), autoincrement=False, nullable=True),
                    sa.Column('registration_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.Column('last_login_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('id', name='users_pkey'),
                    sa.UniqueConstraint('email', name='users_email_key'),
                    sa.UniqueConstraint('username', name='users_username_key'),
                    postgresql_ignore_search_path=False
                    )
    op.create_table('addresses',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('country', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
                    sa.Column('province_or_state', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
                    sa.Column('city', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
                    sa.Column('street', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
                    sa.Column('postal_code', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
                    sa.Column('is_default', sa.BOOLEAN(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='addresses_user_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='addresses_pkey')
                    )
    op.drop_table('order_detail')
    op.drop_table('order')
    op.drop_index(op.f('ix_cart_id'), table_name='cart')
    op.drop_table('cart')
    op.drop_table('address')
    op.drop_index(op.f('ix_verification_code_id'), table_name='verification_code')
    op.drop_table('verification_code')
    op.drop_table('user')
    op.drop_index(op.f('ix_token_id'), table_name='token')
    op.drop_table('token')
    op.drop_index(op.f('ix_goods_info_id'), table_name='goods_info')
    op.drop_table('goods_info')
    # ### end Alembic commands ###
