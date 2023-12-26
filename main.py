import subprocess

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.v1 import test_route, user_route, auth_route,search_route,goods_route
from app.utils.email_utils import account

app = FastAPI()

# 添加路由
app.include_router(user_route.router)  # 添加用户管理模块的路由
app.include_router(auth_route.router)  # 添加认证模块的路由
app.include_router(test_route.router)  # 添加测试模块的路由，用于判断服务是否正常运行
app.include_router(search_route.router)  # 添加用户检索模块的路由
app.include_router(goods_route.router) #添加商品管理模块路由



@app.get("/")
async def read_root():
    html_file_path = "assets/index.html"
    return FileResponse(html_file_path)


@app.on_event("startup")
async def startup_event():
    """初始化：数据库"""
    try:
        print("Start to initialize database...")
        alembic_command = "alembic upgrade head"
        subprocess.run(alembic_command, shell=True, check=True)
        print("Database initialization completed!")
    except:
        pass
    # except subprocess.CalledProcessError as e:
    #     print(f"Error while initializing database: {e}")
    # if not account.is_authenticated:
    #     account.authenticate()
