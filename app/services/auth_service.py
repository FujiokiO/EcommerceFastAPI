"""认证服务逻辑：services/auth_service.py"""
import os
from datetime import datetime, timedelta
from typing import Union

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.db.crud.user_crud import get_user_by_name, insert_verification_code
from app.models.token_model import TokenData
from app.models.user_model import BaseUser, UserInDB

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> Union[UserInDB, str]:
    user = get_user_by_name(username)
    if not user:
        return "User not found"
    if not verify_password(password, user.hashed_password):
        return "Incorrect password"
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data.username


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """获取当前用户：管理员或正常用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 调用异步函数 get_current_token 并等待其返回结果
        username = await get_current_token(token)
        user = get_user_by_name(username, mode='normal')
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


async def get_current_user_db(token: str = Depends(oauth2_scheme)):
    """获取当前用户的数据库类型：管理员或正常用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = await get_current_token(token)
        user = get_user_by_name(username)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


async def get_current_active_user(current_user: BaseUser = Depends(get_current_user)):
    """获取当前用户：正常用户"""
    if current_user.is_disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def generate_verification_code():
    """生成6位数的验证码"""
    import random
    return "".join([str(random.randint(0, 9)) for _ in range(6)])


def save_verification_code(email: str, code: str):
    """保存验证码"""
    insert_verification_code(email, code)
