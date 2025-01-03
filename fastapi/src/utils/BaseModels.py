from pydantic import BaseModel, Field, field_validator
from typing import List
from fastapi import (UploadFile, File)
from fastapi.responses import FileResponse
from . import Error_handlers as error_handlers

filename= Field(
    title="파일 이름",
    description="요청된 파일의 이름",
    examples=["example.png"]
)

folder = Field(
    title="폴더 이름",
    description="정적 파일이 포함된 폴더의 이름",
    examples=["images"]
)

folders = Field(
    title="폴더 리스트",
    description="static 폴더 내의 하위 디렉토리 리스트",
    examples=[["images", "docs"]]
)

images = Field(
    title="이미지 파일 리스트",
    description="지정된 폴더 내 이미지 파일들의 리스트",
    examples=[["example.png", "sample.jpg"]]
)

class FolderResponse(BaseModel):
    '''
    폴더 응답 모델
    folders: 폴더 이름들의 리스트
    '''
    folders: List[str] = folders

class FolderRequest(BaseModel):
    '''
    폴더 요청 모델
    folder: 폴더 이름
    '''
    folder: str = folder

class ImageListResponse(BaseModel):
    '''
    이미지 리스트 응답 모델
    images: 이미지 파일 이름들의 리스트
    '''
    images: List[str] = images
    

class ImageRequest(BaseModel):
    '''
    이미지 요청 모델
    folder: 폴더 이름
    filename: 파일 이름
    '''
    folder: str = folder
    filename: str = filename

    @field_validator('filename', mode='before')
    def validate_file_extension(cls, value):
        '''
        파일 확장자 유효성 검사기
        '''
        allowed_extensions = {"png", "jpg", "jpeg", "gif", "bmp", "tiff", "webp", "svg", "ico"}
        if "." not in value or value.split(".")[-1].lower() not in allowed_extensions:
            raise error_handlers.ValueErrorException(
                detail=f"'{value}'는 유효한 이미지 파일 이름이 아닙니다. 허용되는 확장자: {', '.join(allowed_extensions)}"
            )
        return value

    @field_validator('folder', mode='before')
    def validate_folder(cls, value):
        if not value.strip():
            raise error_handlers.ValueErrorException(detail="폴더 이름은 비어 있을 수 없습니다.")
        return value
    
class ImageResponse(FileResponse):
    def __init__(self, path: str, *args, **kwargs):
        super().__init__(path, *args, **kwargs)
