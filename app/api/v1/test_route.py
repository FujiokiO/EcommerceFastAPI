import os
import re

import requests
from dotenv import load_dotenv
from fastapi import HTTPException, Response, APIRouter

router = APIRouter()


# API 端点：获取 Markdown 文件并转换为 HTML
@router.get("/test/md-post/", tags=["测试模块"])
async def get_markdown_post(markdown_url: str):
    try:
        # 获取 Markdown 文件内容
        response = requests.get(markdown_url, timeout=5)  # 设置请求超时时间为 10 秒
        response.raise_for_status()  # 检查请求状态

        markdown_content = response.text

        # 检查 Markdown 文件大小
        if len(markdown_content) > 1024 * 1024:  # 限制文件大小为 1MB
            raise HTTPException(status_code=400, detail="Markdown file size exceeds the limit")

        # 从 Markdown 文件中提取第一个一级标题作为 HTML 页面标题
        match = re.search(r"^# (.+)$", markdown_content, re.MULTILINE)
        if match:
            title = match.group(1)
        else:
            title = "Post with Github Style"

        # 使用 GitHub API 将 Markdown 转换为 HTML（使用 GFM 模式）
        github_api_url = "https://api.github.com/markdown"
        load_dotenv()
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": os.getenv('GITHUB_TOKEN')
        }
        data = {
            "text": markdown_content,
            "mode": "gfm"  # 使用 GFM 模式
        }
        github_response = requests.post(github_api_url, headers=headers, json=data)
        github_response.raise_for_status()  # 检查 GitHub API 请求状态

        html_content = github_response.text

        # 构建完整的 HTML 结构，设置页面语言为中文，并添加内联 CSS 样式
        complete_html = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <title>{title} - POST | OKY</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                header {{
                    background-color: #0d6e00;
                    color: #fff;
                    padding: 20px 0;
                    text-align: center;
                }}
                main {{
                    padding: 20px 0;
                }}
                footer {{
                    background-color: #0d6e00;
                    color: #fff;
                    padding: 10px 0;
                    text-align: center;
                }}
                h1 {{
                    margin-bottom: 20px;
                }}
                p {{
                    font-size: 1.1rem;
                    line-height: 1.6;
                }}
                .container {{
                    max-width: 800px;
                }}
                @media (max-width: 767px) {{
                    /* 适应小屏幕设备 */
                    header h1 {{
                        font-size: 28px;
                    }}
                    main {{
                        font-size: 16px;
                    }}
                }}
            </style>
        </head>
        <body>
            <header>
                <div class="container">
                    <h1>{title}</h1>
                </div>
            </header>
            <main class="container">
                {html_content}
            </main>
            <footer>
                <div class="container">
                    &copy; 2023 POST | OKY. All rights reserved.
                </div>
            </footer>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        """

        return Response(content=complete_html, media_type="text/html")

    except requests.Timeout:
        raise HTTPException(status_code=408, detail="Request to Markdown file timed out")

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
