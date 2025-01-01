import os
import yaml
import uvicorn
import asyncio
import platform
from typing import List
from dotenv import load_dotenv
from mimetypes import guess_type

from fastapi import (FastAPI, HTTPException, Request, Depends)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.base import BaseHTTPMiddleware

from utils import base_models, error_handlers

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv() # .env 파일 로드
SSL_PW = os.getenv("SSL_PW")  # 환경변수에서 API 키 가져오기
key_pem = os.getenv("KEY_PEM")  # 환경변수에서 PEM 키 가져오기
crt_pem = os.getenv("CRT_PEM")  # 환경변수에서 PEM 키 가져오기

def load_bot_list(file_path: str) -> list:
    '''
    YAML 파일에서 봇 리스트를 불러오는 함수
    '''
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        return [bot['name'].lower() for bot in data.get('bot_user_agents', [])]

app = FastAPI()
error_handlers.add_exception_handlers(app)  # 예외 핸들러 추가

class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as e:
            return await error_handlers.generic_exception_handler(request, e)
        except Exception as e:
            return await error_handlers.generic_exception_handler(request, e)


app.add_middleware(ExceptionMiddleware)

# 정적 파일 제공 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="ChatBot-AI FastAPI",
        version="v1.0.0",
        summary="Img 반환 API",
        routes=app.routes,
        description=(
            "이 API는 다음과 같은 기능을 제공합니다:\n\n"
            "각 엔드포인트의 자세한 정보는 해당 엔드포인트의 문서에서 확인할 수 있습니다."
        ),
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://drive.google.com/thumbnail?id=12PqUS6bj4eAO_fLDaWQmoq94-771xfim"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.middleware("http")
async def ip_restrict_and_bot_blocking_middleware(request: Request, call_next):
    bot_file_path = os.path.join(os.getcwd(), "bot.yaml")
    bot_user_agents = load_bot_list(bot_file_path)
    user_agent = request.headers.get("User-Agent", "").lower()

    try:
        if any(bot in user_agent for bot in bot_user_agents):
            raise error_handlers.BadRequestException(detail=f"{user_agent} Bot access is not allowed.")

        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    except ConnectionResetError:
        raise error_handlers.ConnectionResetException()
    except HTTPException as e:
        return await error_handlers.generic_exception_handler(request, e)
    except Exception as e:
        return await error_handlers.generic_exception_handler(request, HTTPException(
            status_code=500,
            detail="Internal server error occurred."
        ))

@app.get("/")
async def root():
    return {"message": "Welcome to the Img_API"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    브라우저 탭에 표시되는 파비콘 제공
    """
    favicon_path = os.path.join(static_dir, "favicon.ico")
    return FileResponse(favicon_path)

@app.get("/folders", response_model=base_models.FolderResponse)
async def get_folders():
    """
    static 폴더 내부의 하위 디렉토리 리스트 반환
    """
    try:
        folders = [
            folder for folder in os.listdir(static_dir)
            if os.path.isdir(os.path.join(static_dir, folder))
        ]
        return base_models.FolderResponse(folders=folders)
    except Exception as e:
        raise HTTPException(status_code=500, detail="디렉토리 리스트를 가져오는 중 오류가 발생했습니다.")

@app.post("/folders/images", response_model=base_models.ImageListResponse)
async def get_images_in_folder(request: base_models.FolderRequest):
    """
    지정된 폴더 내 이미지 파일 리스트 반환
    """
    folder_path = os.path.join(static_dir, request.folder)

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        raise HTTPException(status_code=404, detail="지정된 폴더를 찾을 수 없습니다.")

    try:
        images = [
            file for file in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, file)) and file.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
        ]
        return base_models.ImageListResponse(images=images)
    except Exception as e:
        raise HTTPException(status_code=500, detail="이미지 리스트를 가져오는 중 오류가 발생했습니다.")

@app.get("/{folder}/{filename}")
async def get_image(request: Request, image_request: base_models.ImageRequest = Depends()):
    """
    지정된 폴더의 이미지를 반환하여 웹페이지 및 마크다운에서 표시
    """
    try:
        file_path = os.path.join(static_dir, image_request.folder, image_request.filename)

        # 파일 존재 여부 확인
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise error_handlers.NotFoundException(detail="파일을 찾을 수 없습니다.")

        # MIME 타입 확인
        mime_type, _ = guess_type(file_path)
        return base_models.ImageResponse(
            path=file_path,
            media_type=mime_type or "application/octet-stream",
            headers={"Content-Disposition": "inline"}
        )

    except HTTPException as http_exc:
        return await error_handlers.generic_exception_handler(request, http_exc)

    except Exception as exc:
        # 기타 예외 처리
        return await error_handlers.generic_exception_handler(request, HTTPException(
            status_code=500,
            detail="파일을 가져오는 중 예상치 못한 오류가 발생했습니다."
        ))

if __name__ == "__main__":
    # certificates_dir = os.path.abspath(
    #     os.path.join(os.path.dirname(__file__), "..", "..", "certificates")
    # )
    # ssl_keyfile = os.path.join(certificates_dir, key_pem)
    # ssl_certfile = os.path.join(certificates_dir, crt_pem)
    #
    # config = uvicorn.Config(
    #     app,
    #     host="0.0.0.0",
    #     port=442,  # HTTPS 기본 포트
    #     ssl_keyfile=ssl_keyfile,
    #     ssl_certfile=ssl_certfile,
    #     loop="asyncio",
    #     http="h11"
    # )
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,  # FastAPI는 HTTP로 실행
        loop="asyncio",
        http="h11"
    )
    server = uvicorn.Server(config)
    server.run()
