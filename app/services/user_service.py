"""用户服务逻辑：services/user_service.py"""
from typing import List

from app.db.crud.user_crud import insert_user, check_existing_user_by_email, check_existing_user_by_name, \
    update_user_by_id, \
    select_all_users, is_valid_verification_code, update_password_by_username
from app.models.user_model import RegisterUser, BaseUser
from app.services.auth_service import get_password_hash


def is_valid_password(password: str) -> bool:
    """验证密码强度的函数，可以根据实际需求进行扩展"""
    # 例如：密码长度至少为8位，包含大小写字母、数字和特殊字符
    return len(password) >= 8 and any(c.isupper() for c in password) and any(c.islower() for c in password) and any(
        c.isdigit() for c in password) and any(not c.isalnum() for c in password)


def register_new_user(user: RegisterUser) -> BaseUser:
    """用户注册服务逻辑：验证用户信息并将其注册到数据库"""
    if check_existing_user_by_email(user.email):
        raise ValueError("该邮箱已被注册")
    if check_existing_user_by_name(user.username):
        raise ValueError("该用户名已被注册")
    if not is_valid_password(user.password):
        raise ValueError("密码不符合要求")
    if not is_valid_verification_code(user.email, user.verification_code):
        raise ValueError("验证码错误")

    # 对团队成员添加管理员权限
    whitelisted_domains = ["oky.services", "dbcd.oky.wiki"]
    domain = user.email.split("@")[-1]
    user.is_admin = domain in whitelisted_domains

    # 对用户密码进行哈希加密
    user.hashed_password = get_password_hash(user.password)

    # 调用 CRUD 操作函数创建新用户
    return insert_user(user)


def reset_password(current_user: str, user_email: str, verification_code: str, new_password: str) -> bool:
    """重置用户密码的服务逻辑"""
    if not is_valid_verification_code(current_user, verification_code):
        raise ValueError("验证码错误")
    if not is_valid_password(new_password):
        raise ValueError("密码不符合要求")
    return update_password_by_username(user_email, get_password_hash(new_password))


def update_user_info(user_id: int, new_data: BaseUser) -> BaseUser:
    """更新用户信息的服务逻辑"""
    return update_user_by_id(user_id, new_data.__dict__)


def fetch_all_users() -> List[BaseUser]:
    """获取所有用户信息的服务逻辑"""
    return select_all_users()
