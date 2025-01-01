# Windows에서 FastAPI의 HTTPS 설정 방법 (win-acme 사용)

이 문서는 **win-acme**(Windows용 ACMEv2 클라이언트)을 사용하여 Let's Encrypt로부터 SSL 인증서를 생성하고 FastAPI 애플리케이션에 HTTPS를 설정하는 방법을 설명합니다.

## 사전 준비 사항

- Windows 환경
- 관리자 권한 (일부 단계에서 필요)
- win-acme 클라이언트 설치 ([win-acme GitHub](https://github.com/win-acme/win-acme)에서 다운로드)
- 서버에 연결된 도메인 이름 (예: `example.com`)
- Python의 `python-dotenv` 라이브러리 설치 (.env 파일 관리를 위해 필요)

## HTTPS 설정 단계

### 1. win-acme 실행

1. win-acme이 설치된 디렉터리로 이동합니다.
2. win-acme 실행 파일을 실행합니다:
   ```bash
   .\wacs.exe
   ```

### 2. 인증서 생성 옵션 선택

다음과 같이 옵션을 선택합니다:

#### 메뉴 옵션

- **N:** 기본 설정으로 인증서 생성
- **M:** 전체 옵션으로 인증서 생성 *(고급 설정을 원할 경우 선택)*

#### 도메인 선택

1. **수동 입력**: 도메인을 직접 입력합니다.
   ```
   Host: example.com
   ```

#### 인증서 분할 옵션

- `4: 단일 인증서`를 선택하여 모든 도메인을 포함하는 단일 인증서를 생성합니다.

### 3. 소유권 검증 방법

도메인 소유권을 검증하기 위해 방법을 선택합니다:

1. **HTTP 검증 (http-01)**
   - `1: 네트워크 경로에 검증 파일 저장`을 선택합니다.
   - 사이트의 루트 경로를 설정합니다:
     ```
     Path: <프로젝트 디렉터리 경로>
     ```
   - `web.config` 파일을 복사하라는 메시지가 표시되면:
     ```
     복사하시겠습니까? (y/n): y
     ```

### 4. 키 유형

인증서의 개인 키 유형을 선택합니다:

- **2: RSA 키** *(권장)*

### 5. 인증서 저장

인증서를 저장할 방법을 선택합니다:

1. **PEM 형식 파일** *(FastAPI 및 기타 Python 프레임워크에서 사용)*:

   - `.pem` 파일을 저장할 경로를 설정합니다:
     ```
     File path: ./certificates
     ```
   - 비밀번호를 묻는 메시지에서:
     ```
     1: 비밀번호 없음
     ```

2. 추가 저장 옵션은:

   ```
   다른 저장 방식도 사용하시겠습니까?: 5
   ```

### 6. 인증서 설치 완료

인증서가 생성되면, 지정한 폴더(`./certificates`)에 다음 파일이 생성됩니다:

- `fullchain.pem`: 인증서 체인
- `privkey.pem`: 개인 키

### 7. FastAPI에 HTTPS 구성

1. `.pem` 파일을 `./certificates` 디렉터리로 이동합니다.

2. `.env` 파일을 생성하여 환경 변수를 저장합니다:

   ```env
   SSL_PW=
   KEY_PEM=privkey.pem
   CRT_PEM=fullchain.pem
   ```

   #### `.env` 파일 변수 설명
   - `SSL_PW`: SSL 인증서에 비밀번호가 설정된 경우 해당 비밀번호를 입력합니다. 비밀번호가 없다면 비워둡니다.
   - `KEY_PEM`: 개인 키 파일 이름입니다. 기본적으로 `privkey.pem`으로 설정됩니다.
   - `CRT_PEM`: 인증서 파일 이름입니다. 기본적으로 `fullchain.pem`으로 설정됩니다.

3. FastAPI 애플리케이션 코드를 업데이트합니다:

```python
import os
from dotenv import load_dotenv
import uvicorn

# 환경 변수 로드
load_dotenv()
SSL_PW = os.getenv("SSL_PW")  # SSL 비밀번호 (필요한 경우)
key_pem = os.getenv("KEY_PEM")  # 개인 키 PEM 파일 이름
crt_pem = os.getenv("CRT_PEM")  # 인증서 PEM 파일 이름

# ... 중간 코드드

if __name__ == "__main__":
    certificates_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "certificates")
    )
    ssl_keyfile = os.path.join(certificates_dir, key_pem)
    ssl_certfile = os.path.join(certificates_dir, crt_pem)

    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=443,  # HTTPS 기본 포트
        ssl_keyfile=ssl_keyfile,
        ssl_certfile=ssl_certfile,
        loop="asyncio",
        http="h11"
    )
    server = uvicorn.Server(config)
    server.run()
```

### 8. 인증서 갱신

win-acme은 자동 갱신을 지원하며, 예약 작업으로 설정할 수 있습니다. 예약 작업을 확인하려면:

1. win-acme을 열고 `A: 갱신 관리`를 선택합니다.
2. 설정된 갱신 작업을 검토하고 올바르게 구성되었는지 확인합니다.

### 참고 사항

- 방화벽에서 HTTPS를 위한 포트 443의 트래픽을 허용해야 합니다.
- win-acme을 관리자 권한으로 실행하면 IIS 통합과 같은 추가 옵션을 사용할 수 있습니다.
- `https://your-domain`으로 애플리케이션에 접근하여 설정을 테스트하세요.