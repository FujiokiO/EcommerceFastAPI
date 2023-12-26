"""认证路由：api/auth_route.py"""
import os
from datetime import timedelta

from O365 import Account
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.db.crud.mail_crud import PostgresBackend
from app.models.token_model import *
from app.services import auth_service, user_service

load_dotenv()
callback = os.getenv('API_URL') + "/auth/microsoft/callback"
client_id = os.getenv('MICROSOFT_CLIENT_ID')
client_secret = os.getenv('MICROSOFT_CLIENT_SECRET')
credentials = (client_id, client_secret)

# 使用你的凭据创建 Account 对象
scopes = ['https://graph.microsoft.com/Mail.ReadWrite', 'https://graph.microsoft.com/Mail.Send']
account = Account(credentials, token_backend=PostgresBackend(), scopes=scopes)

router = APIRouter()


class MyDB:
    state = None


my_db = MyDB()


@router.post("/auth", tags=["认证模块"], response_model=Token)
async def auth_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """用户认证路由"""
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if isinstance(user, str):
        error_message = user
        if error_message == "User not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        elif error_message == "Incorrect password":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
                headers={"WWW-Authenticate": "Bearer"}
            )
    else:
        access_token_expires = timedelta(minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_service.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


@router.post("/reset-password", tags=["认证模块"])
async def reset_password(user_email: EmailStr, verification_code: str, new_password: str):
    success = user_service.reset_password(user_email, user_email, verification_code, new_password)
    if success:
        return {"message": "Password reset request sent"}
    else:
        return {"message": "Reset request failed"}


@router.get("/auth/microsoft", tags=["认证模块"])
async def auth_microsoft():
    url, state = account.con.get_authorization_url(requested_scopes=scopes, redirect_uri=callback)
    my_db.state = state
    return RedirectResponse(url)


@router.get("/auth/microsoft/callback", tags=["认证模块"])
async def auth_microsoft_fallback(request: Request):
    request_url = str(request.url)
    result = account.con.request_token(
        authorization_url=request_url,
        state=my_db.state,
        redirect_uri=callback
    )
    if result:
        return {"message": "Authentication successful. Token stored."}
    else:
        raise HTTPException(status_code=400, detail="Authentication failed.")
