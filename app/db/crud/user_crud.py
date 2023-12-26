from typing import List, Union

from sqlalchemy import text

from app.db.base import SessionLocal
from app.models.user_model import RegisterUser, UserInDB, BaseUser


def insert_user(user: RegisterUser) -> BaseUser:
    """创建新用户并将其添加到数据库"""
    db = SessionLocal()
    insert_query = text('INSERT INTO "user" (username, email, is_disabled, is_admin, password) VALUES '
                        '(:username, :email, :is_disabled, :is_admin, :password)')
    db.execute(insert_query, {
        'username': user.username,
        'email': user.email,
        'is_disabled': user.is_disabled,
        'is_admin': user.is_admin,
        'password': user.hashed_password
    })
    db.commit()
    db.close()
    return BaseUser(username=user.username, email=user.email,
                    is_disabled=user.is_disabled, is_admin=user.is_admin)


def get_user_by_name(username: str, mode: str = None) -> Union[UserInDB, BaseUser, None]:
    """根据用户名从数据库中获取用户信息"""
    db = SessionLocal()
    select_query = text('SELECT id, username, email, password, is_disabled, is_admin FROM "user" '
                        'WHERE username = :username')
    user_row = db.execute(select_query, {'username': username}).fetchone()
    db.close()
    if user_row:
        user_data = {
            'id': user_row.id,
            'username': user_row.username,
            'email': user_row.email,
            'hashed_password': user_row.password,
            'is_disabled': user_row.is_disabled,
            'is_admin': user_row.is_admin
        }
        if mode == 'normal':
            return BaseUser(**dict(user_data))
        else:
            return UserInDB(**dict(user_data))
    else:
        return None


def select_all_users() -> List[BaseUser]:
    """从数据库中获取所有用户信息"""
    db = SessionLocal()
    select_all_query = text('SELECT id, username, email, password, is_disabled, is_admin FROM "user"')
    users_data = db.execute(select_all_query).fetchall()
    db.close()
    users_db = [
        BaseUser(
            id=user_tuple[0],
            username=user_tuple[1],
            email=user_tuple[2],
            password=user_tuple[3],
            is_disabled=user_tuple[4],
            is_admin=user_tuple[5]
        )
        for user_tuple in users_data
    ]
    return users_db


def check_existing_user_by_email(email: str) -> bool:
    """根据邮箱判断用户是否存在"""
    db = SessionLocal()
    select_query = text('SELECT COUNT(*) FROM "user" WHERE email = :email')
    count = db.execute(select_query, {'email': email}).fetchone()[0]
    db.close()
    return count > 0


def check_existing_user_by_name(username: str) -> bool:
    """根据用户名判断用户是否存在"""
    db = SessionLocal()
    select_query = text('SELECT COUNT(*) FROM "user" WHERE username = :username')
    count = db.execute(select_query, {'username': username}).fetchone()[0]
    db.close()
    return count > 0


def is_valid_verification_code(email: str, code: str) -> bool:
    db = SessionLocal()
    try:
        query = text('SELECT id FROM verification_code WHERE email = :email AND code = :code AND is_used = FALSE '
                     'AND expiration_time > CURRENT_TIMESTAMP')
        result = db.execute(query, {"email": email, "code": code}).fetchone()

        if result:
            # 如果存在有效的验证码，将 is_used 标记为已使用
            verification_code_id = result[0]
            update_query = text('UPDATE verification_code SET is_used = TRUE WHERE id = :id')
            db.execute(update_query, {"id": verification_code_id})
            db.commit()
            return True
        else:
            return False
    finally:
        db.close()


def insert_verification_code(email: str, code: str):
    db = SessionLocal()
    try:
        query = text("""
            INSERT INTO verification_code (email, code, created_at, expiration_time, is_used) 
            VALUES (:email, :code, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '10 MINUTE', FALSE)
            ON CONFLICT (email) DO UPDATE
            SET 
                code = :code,
                created_at = CURRENT_TIMESTAMP,
                expiration_time = CURRENT_TIMESTAMP + INTERVAL '10 MINUTE',
                is_used = FALSE
            WHERE 
                verification_code.email = EXCLUDED.email
        """)
        db.execute(query, {"email": email, "code": code})
        db.commit()
    finally:
        db.close()


def update_user_by_id(user_id: int, new_data: dict) -> BaseUser:
    """根据用户ID更新用户信息"""
    db = SessionLocal()
    update_query = text('UPDATE "user" SET username = :username, email = :email '
                        'WHERE id = :user_id')
    db.execute(update_query, {
        'username': new_data['username'],
        'email': new_data['email'],
        'user_id': user_id
    })
    db.commit()

    return get_user_by_name(new_data['username'], mode='normal')


def update_password_by_username(user_email: str, new_password: str) -> bool:
    """根据用户邮箱更新用户密码"""
    db = SessionLocal()
    try:
        update_query = text('UPDATE "user" SET password = :password WHERE email = :email')
        db.execute(update_query, {'password': new_password, 'email': user_email})
        db.commit()
        affected_rows = db.execute("SELECT ROW_COUNT()").fetchone()[0]
        return affected_rows > 0
    finally:
        db.close()
