from pydantic import BaseModel, Field, field_validator

class ImageRequest(BaseModel):
    folder: str = Field(
        title="폴더 이름",
        description="정적 파일이 포함된 폴더의 이름",
        examples=["images"]
    )
    filename: str = Field(
        title="파일 이름",
        description="요청된 파일의 이름",
        examples=["example.png"]
    )
    @field_validator('filename', mode='before')
    def validate_file_extension(cls, value):
        allowed_extensions = {"png", "jpg", "jpeg", "gif", "bmp", "tiff", "webp", "svg", "ico"}
        if "." not in value or value.split(".")[-1].lower() not in allowed_extensions:
            raise ValueError(f"'{value}'는 유효한 이미지 파일 이름이 아닙니다. 허용되는 확장자: {', '.join(allowed_extensions)}")
        return value

    def model_dump(self, **kwargs):
        """
        Pydantic BaseModel의 dict() 메서드를 대체하는 model_dump() 메서드입니다.
        필터링된 데이터만 반환하도록 수정할 수 있습니다.
        """
        return super().model_dump(**kwargs)

class ImageResponse(BaseModel):
    file_path: str = Field(
        title="파일 경로",
        description="정적 파일의 전체 경로",
        examples=["src/static/images/example.png"]
    )
