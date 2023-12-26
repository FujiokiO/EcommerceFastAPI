"""用户路由：api/user_route.py"""

from typing import List

from fastapi import APIRouter, HTTPException, Depends

from app.models.user_model import *
from app.services import user_service, auth_service
from app.utils import email_utils

router = APIRouter()


@router.post("/send-verification-code", tags=["用户管理模块"])
async def send_verification_code(email: str):
    """发送验证码路由"""
    verification_code = auth_service.generate_verification_code()

    success = email_utils.send_verification_email(email, verification_code)
    if success:
        auth_service.save_verification_code(email, verification_code)
        return {"message": "Verification code sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send verification code, please try again later")


@router.post("/register", tags=["用户管理模块"])
async def register_user(username: str, password: str, email: EmailStr, verification_code: str):
    """用户注册路由"""
    user = RegisterUser(
        username=username,
        password=password,
        email=email,
        verification_code=verification_code
    )
    try:
        new_user = user_service.register_new_user(user)
        if new_user is None:
            raise HTTPException(status_code=404, detail="Failed to register user")
        if new_user.is_admin:
            return {
                "username": new_user.username,
                "message": "Admin user registered successfully."
            }
        else:
            return {
                "username": new_user.username,
                "message": "User registered successfully."
            }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/me", tags=["用户管理模块"], response_model=BaseUser)
async def get_user_info(current_user: BaseUser = Depends(auth_service.get_current_active_user)):
    """用户信息获取路由"""
    return current_user


@router.get("/user/all", tags=["用户管理模块"], response_model=List[BaseUser])
async def get_all_users_info(current_user: BaseUser = Depends(auth_service.get_current_active_user)):
    """用户信息获取路由"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    all_users = user_service.fetch_all_users()
    return all_users


@router.put("/user/me", tags=["用户管理模块"], response_model=BaseUser)
async def update_user_info(new_username: str = None, new_email: EmailStr = None,
                           current_user: UserInDB = Depends(auth_service.get_current_user_db)):
    """用户信息更新路由"""
    # 检查新用户名和新电子邮件是否为空，如果不为空，才创建新的用户信息对象
    if new_username is not None or new_email is not None:
        user_info = BaseUser(
            username=new_username or current_user.username,
            email=new_email or current_user.email,
            is_disabled=current_user.is_disabled,
            is_admin=current_user.is_admin
        )
        updated_user = user_service.update_user_info(current_user.id, user_info)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    else:
        raise HTTPException(status_code=400, detail="Both username and email cannot be empty")


@router.post("/user/reset-password", tags=["用户管理模块"])
async def reset_user_password(verification_code: str, new_password: str, user_email: EmailStr = None,
                              current_user: UserInDB = Depends(auth_service.get_current_user_db)):
    """密码重置路由"""
    if not current_user.is_admin:
        if user_email == current_user.email or user_email is None:
            user_email = current_user.email
        else:
            raise HTTPException(status_code=403, detail="Permission denied")
    else:
        if user_email is None:
            raise HTTPException(status_code=400, detail="Email not provided")
    success = user_service.reset_password(current_user.email, user_email, verification_code, new_password)
    if success:
        return {"message": "Password reset request sent"}
    else:
        return {"message": "Reset request failed"}
