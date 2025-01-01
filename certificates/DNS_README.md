# DNS 설정 가이드 (no-ip에서 도메인 생성)

이 문서는 no-ip를 사용하여 무료 도메인을 생성하고 DNS 설정을 구성하는 방법을 설명합니다. DNS 설정은 외부 도메인과 서버를 연결하고 HTTPS와 같은 안전한 통신 환경을 제공하기 위해 필수적인 과정입니다.

## 1. no-ip에서 계정 생성

1. [no-ip](https://www.noip.com/) 웹사이트에 접속합니다.
2. "Sign Up" 버튼을 클릭하여 계정을 생성합니다.
   - 이메일 주소, 비밀번호 등을 입력하고 계정을 등록합니다.
3. 이메일로 전송된 인증 링크를 클릭하여 계정을 활성화합니다.

## 2. 무료 도메인 생성

1. 로그인 후 **Dynamic DNS** 페이지로 이동합니다.
2. "Create Hostname" 또는 "Add a Host" 버튼을 클릭합니다.
3. 아래와 같은 정보를 입력합니다:
   - **Hostname**: 원하는 도메인 이름 (예: `example.ddns.net`)
   - **Domain**: 제공된 도메인 중 하나를 선택 (예: `ddns.net`)
   - **IPv4 Address**: 서버의 공인 IP 주소를 입력

4. 설정을 완료하고 "Save" 버튼을 클릭합니다.

## 3. DNS 설정 확인

1. 생성한 도메인이 올바르게 작동하는지 확인하려면 터미널에서 다음 명령어를 실행합니다:
   ```bash
   ping example.ddns.net
   ```
2. 서버의 IP 주소가 반환되면 설정이 성공적으로 완료된 것입니다.

## 4. A 레코드 업데이트 (필요한 경우)

1. no-ip의 DNS 관리 페이지에서 A 레코드를 추가하거나 수정합니다.
2. 아래와 같은 형식으로 입력합니다:

   | 레코드 타입 | 호스트 이름 | 값           | TTL  |
   |-------------|-------------|--------------|------|
   | A           | @           | 123.45.67.89 | 600  |

   - **호스트 이름(@)**: 루트 도메인을 의미합니다.
   - **값**: 서버의 공인 IP 주소를 입력합니다.
   - **TTL**: 기본값(600초)을 유지합니다.

3. 설정을 저장합니다.

## 5. HTTPS 사용을 위한 TXT 레코드 설정 (필요 시)

Let's Encrypt 인증서 발급을 위해 TXT 레코드를 추가해야 할 수도 있습니다.

1. no-ip의 DNS 관리 페이지에서 TXT 레코드를 추가합니다.
2. 아래와 같은 형식으로 입력합니다:

   | 레코드 타입 | 호스트 이름       | 값                      | TTL  |
   |-------------|-------------------|-------------------------|------|
   | TXT         | _acme-challenge  | 인증용 값               | 600  |

   - **호스트 이름**: `_acme-challenge`를 입력합니다.
   - **값**: 인증서 발급 시 제공된 인증용 값을 입력합니다.

3. 설정을 저장하고, DNS 변경 사항이 전파될 때까지 기다립니다.

## 6. 설정 확인

1. 설정이 완료되었는지 확인하려면 [DNS Checker](https://dnschecker.org)를 사용하여 레코드 상태를 확인합니다.
2. 해당 도메인에 대해 A, TXT 레코드가 올바르게 설정되었는지 확인합니다.

## 7. 참고 사항

- no-ip의 무료 플랜에서는 30일마다 도메인을 갱신해야 합니다.
- DNS 설정이 제대로 반영되기까지 최대 48시간이 걸릴 수 있습니다.
- 잘못된 설정으로 인해 도메인 접속이 불가능할 수 있으니, 설정 후 반드시 확인하세요.

이 가이드를 따라 DNS 설정을 완료한 후 도메인을 사용하여 안전한 HTTPS 통신을 진행할 수 있습니다.
