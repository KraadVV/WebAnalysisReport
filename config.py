# config.py
import os
import sys

# [중요] EXE로 실행 중인지, 파이썬 코드로 실행 중인지 확인하여 경로 설정
if getattr(sys, 'frozen', False):
    # EXE로 실행될 경우: 실행 파일이 있는 위치가 기준
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # 파이썬으로 실행될 경우: 파일이 있는 위치가 기준
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 기본 분석 URL (입력이 없을 경우 사용)
TARGET_URL = "https://www.google.com"

# 브라우저 설정
HEADLESS_MODE = True # 배포 시에는 True(화면 숨김)로 바꾸는 것을 추천하지만, 테스트 땐 False 유지
VIEWPORT_SIZE = {"width": 1280, "height": 720}
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# 파일 저장 경로 설정
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
SCREENSHOT_DIR = os.path.join(OUTPUT_DIR, "screenshots")

# 폴더가 없으면 생성
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# SNS 분석 설정
SNS_VALIDATE_LINKS = True  # 링크 유효성 검사 수행
SNS_FETCH_METADATA = True  # 프로필 메타데이터 가져오기
SNS_MAX_VALIDATE = 20      # 최대 검증할 링크 수
SNS_MAX_METADATA = 10      # 최대 메타데이터 가져올 링크 수

# 보고서 최적화 설정
MAX_INTERACTIVE_ELEMENTS = 15  # 보고서에 표시할 최대 상호작용 요소 수
FILTER_LANGUAGE_SELECTORS = True  # 언어/국가 선택 링크 필터링
MAX_NETWORK_IPS = 15  # 네트워크 섹션에 표시할 최대 IP 수
SHOW_SNS_IN_CONTACTS = False  # Section 9에 SNS 중복 표시 안 함 (Section 10에만)

# SNS API Keys (선택사항 - 비워두면 기본 웹 스크래핑 사용)
SNS_API_KEYS = {
    'twitter_bearer_token': '',
    'facebook_app_id': '',
    'facebook_app_secret': '',
    'youtube_api_key': '',
    'reddit_client_id': '',
    'reddit_client_secret': '',
    'telegram_bot_token': ''
}
