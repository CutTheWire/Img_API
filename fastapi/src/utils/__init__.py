# Desc: Package initializer for the utils module
'''
utils 패키지 초기화 모듈

이 모듈은 utils 패키지의 초기화를 담당합니다. 다음과 같은 모듈들을 포함하고 있습니다:

- BaseModels: FastAPI 애플리케이션에서 사용되는 Pydantic 모델을 정의합니다.
- Error_handlers: FastAPI 애플리케이션에서 발생하는 예외를 처리하는 모듈입니다.

__all__ 리스트를 통해 외부에서 접근 가능한 모듈들을 정의합니다. \n
__unused__ 리스트를 통해 사용되지 않는 모듈들을 정의합니다.
'''

__version__='1.0.0'

# Used modules
from . import BaseModels as base_models
from . import Error_handlers as error_handlers


__all__ = [
    'base_models',
    'error_handlers'
]