# src/browser_handler.py
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
import time
import sys
import os

# 상위 폴더의 config를 임포트하기 위해 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None

    def launch_browser(self):
        """브라우저를 실행하고 설정을 적용합니다."""
        print("[Browser] Launching browser...")
        self.playwright = sync_playwright().start()

        executable_path = None
        if getattr(sys, 'frozen', False):
            # EXE 실행 시 기준 경로
            base_dir = os.path.dirname(sys.executable)
            # USB 안의 browsers 폴더 경로 지정
            executable_path = os.path.join(base_dir, "chrome-win64", "chrome.exe")

            if not os.path.exists(executable_path):
                print(f"❌ 오류: 브라우저 파일을 찾을 수 없습니다.\n경로: {executable_path}")
                # 파일이 없으면 그냥 진행해서(혹은 종료해서) 에러 메시지를 보게 함

            # launch 옵션에 executable_path 추가
            self.browser = self.playwright.chromium.launch(
                headless=config.HEADLESS_MODE,
                executable_path=executable_path  # 여기가 핵심! None이면 시스템 기본값 사용
            )

            self.context = self.browser.new_context(
                viewport=config.VIEWPORT_SIZE,
                user_agent=config.USER_AGENT
            )

            self.page = self.context.new_page()
            print("[Browser] Browser launched successfully.")

            return self.page


        self.browser = self.playwright.chromium.launch(
            headless=config.HEADLESS_MODE
        )

        # 뷰포트 및 User-Agent 설정
        self.context = self.browser.new_context(
            viewport=config.VIEWPORT_SIZE,
            user_agent=config.USER_AGENT
        )

        self.page = self.context.new_page()
        print("[Browser] Browser launched successfully.")

        return self.page  # 네트워크 스니퍼 등 다른 모듈에서 쓸 수 있게 페이지 객체 반환

    def navigate_to(self, url: str):
        """URL로 이동하고 로딩 완료를 대기합니다."""
        print(f"[Browser] Navigating to: {url}")
        try:
            self.page.goto(url)
            # 네트워크 연결이 유휴 상태가 될 때까지 대기 (최대 10초)
            # 동적 웹사이트(SPA)의 로딩을 기다리기 위해 필수
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as e:
            print(f"[Browser] Error navigating: {e}")

    def capture_screen(self, filename="screenshot.png"):
        """전체 화면 스크린샷을 찍습니다."""
        save_path = os.path.join(config.SCREENSHOT_DIR, filename)

        print("[Browser] Processing Lazy Loading (Scrolling)...")
        self._smooth_scroll()  # 스크롤을 내려서 이미지 로딩 유도

        print(f"[Browser] Taking screenshot: {save_path}")
        self.page.screenshot(path=save_path, full_page=True)

        return save_path

    def extract_interactive_elements(self):
        """
        화면 내의 클릭 가능한 요소(버튼, 링크 등)를 찾아 스크린샷과 동작 정보를 추출합니다.
        """
        print("[Browser] Extracting interactive elements...")

        # 요소 스크린샷 저장 폴더 생성
        elem_dir = os.path.join(config.SCREENSHOT_DIR, "elements")
        os.makedirs(elem_dir, exist_ok=True)

        self._smooth_scroll()
        time.sleep(2)

        interactive_data = []

        selectors = "a, button, input[type='submit'], input[type='button'], [role='button'], [onclick]"
        # 분석 대상: a 태그, button 태그, input(submit/button) 태그
        # 너무 많을 수 있으므로 상위 20개 정도만 제한하거나, 특정 크기 이상인 것만 필터링 가능
        elements = self.page.query_selector_all(selectors)

        print(f"[Browser] Found {len(elements)} potential elements. Filtering...")

        count = 0
        saved_hashes = set()

        for i, elem in enumerate(elements):
            if count >= 30: break  # 보고서 용량 문제로 최대 20개까지만 분석 (조절 가능)

            try:
                # 1. 요소가 화면에 보이는지 확인 (안 보이면 스킵)
                if not elem.is_visible():
                    continue

                # 2. 텍스트 추출
                box = elem.bounding_box()
                if not box or box['width'] < 10 or box['height'] < 10:
                    continue

                text = elem.inner_text().strip()
                if not text:
                    # 텍스트가 없으면(이미지 버튼 등) 태그명이나 ID로 대체
                    text = elem.get_attribute("aria-label") or ""
                    if not text:
                        img = elem.query_selector("img")
                        if img:
                            text = img.get_attribute("alt") or "[기타 이미지]"
                        else:
                            text = f"[{elem.get_attribute('class') or elem.get_attribute('id') or 'Unknown Button'}]"

                text = text[:50].replace("\n", " ")

                # 3. 동작(Action) 정보 추출
                tag_name = elem.evaluate("el => el.tagName").lower()
                action_info = "Click Action"

                href = elem.get_attribute('href')
                onclick = elem.get_attribute('onclick')

                if href and href != "#":
                    action_info = f"Link : {href[:60]}"
                elif onclick:
                    action_info = f"JS: {onclick[:30]}"
                elif tag_name == "button" or elem.get_attribute("role") == "button":
                    action_info = "Button Clock (Script)"

                unique_key = f"{text}-{action_info}"
                if unique_key in saved_hashes:
                    continue
                saved_hashes.add(unique_key)

                # 4. 요소 개별 스크린샷 촬영
                # 파일명 안전하게 변환
                safe_text = "".join(c for c in text if c.isalnum())[:10]
                img_filename = f"elem_{i}_{safe_text}.png"
                img_path = os.path.join(elem_dir, img_filename)

                elem.screenshot(path=img_path)

                interactive_data.append({
                    "id": i,
                    "text": text,
                    "type": tag_name,
                    "action": action_info,
                    "image_path": img_path
                })
                count += 1

            except Exception as e:
                # 요소가 겹치거나 사라진 경우 에러 무시
                continue
        print(f"[Browser] Successfully extracted {len(interactive_data)} elements.")
        return interactive_data

    def get_html_source(self):
        """현재 페이지의 HTML 소스를 반환합니다."""
        return self.page.content()

    def _smooth_scroll(self):
        """
        페이지 최하단까지 부드럽게 스크롤합니다.
        Lazy Loading(지연 로딩) 이미지를 띄우기 위해 필수적입니다.
        """
        self.page.evaluate("""
            async () => {
                await new Promise((resolve) => {
                    var totalHeight = 0;
                    var distance = 100;
                    var timer = setInterval(() => {
                        var scrollHeight = document.body.scrollHeight;
                        window.scrollBy(0, distance);
                        totalHeight += distance;

                        if(totalHeight >= scrollHeight - window.innerHeight){
                            clearInterval(timer);
                            resolve();
                        }
                    }, 50); // 0.05초마다 스크롤 다운
                });
            }
        """)
        # 스크롤 후 렌더링 안정화를 위해 잠시 대기
        time.sleep(1)

    def close(self):
        """브라우저 리소스를 정리합니다."""
        if self.page: self.page.close()
        if self.context: self.context.close()
        if self.browser: self.browser.close()
        if self.playwright: self.playwright.stop()
        print("[Browser] Closed.")