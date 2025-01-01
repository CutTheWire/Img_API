# Img_API

이미지 반환환 API 프로젝트입니다.

## 설치 방법

1. 저장소를 클론합니다.
    ```bash
    git clone https://github.com/yourusername/Img_API.git
    ```
2. 가상 환경을 설정합니다. (PowerShell)
    ```pwsh
    ./batchfile/venv_setup.bat
    ```
3. 필요한 패키지를 설치합니다. (PowerShell)
    ```pwsh
    ./batchfile/venv_install.bat
    ```
4. noip DNS 설정
   
   - [noip DNS 설명](certificates/DNS_README.md)
   
5. wacs.exe로 PEM 설정.

   - [wacs 설명](certificates/PEM_README.md)

## 이미지 관련 참고 문서서

- [Static 폴더 사용 방법](fastapi/src/static/IMG_README.md)


## 사용법

1. 서버를 시작합니다.
    ```bash
    python main.py
    ```
2. 로컬에선 브라우저에서 `https://localhost/docs`에 접속하여 API를 확인합니다.
3. 외부에선 브라우저에서 `https://example.com/docs`에 접속하여 API를 확인합니다.

## 기여 방법

1. 이 저장소를 포크합니다.
2. 새로운 브랜치를 만듭니다.
    ```bash
    git checkout -b feature-branch
    ```
3. 변경 사항을 커밋합니다.
    ```bash
    git commit -m "Add some feature"
    ```
4. 브랜치에 푸시합니다.
    ```bash
    git push origin feature-branch
    ```
5. 풀 리퀘스트를 생성합니다.
