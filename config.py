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