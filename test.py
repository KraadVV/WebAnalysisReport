# main.py
import os
import datetime
from src.browser_handler import BrowserManager
from src.network_sniffer import NetworkTracker
from src.page_analyzer import PageParser
from src.report_writer import DocxGenerator
import config

import config


def main():
    print("=" * 50)
    print("      Web Analysis Automation Tool v1.0")
    print("=" * 50)

    # 1. 사용자로부터 URL 입력 받기
    user_url = input(f"\n분석할 URL을 입력하세요 (엔터키를 치면 기본값 사용):\n[기본값: {config.TARGET_URL}] > ").strip()

    if user_url:
        # http/https가 없으면 자동으로 붙여줌 (편의 기능)
        if not user_url.startswith("http"):
            user_url = "https://" + user_url
        config.TARGET_URL = user_url
        print(f"\n🎯 분석 대상 설정됨: {config.TARGET_URL}")
    else:
        print(f"\n🎯 기본값 사용: {config.TARGET_URL}")

    # 모듈 초기화
    browser_mgr = BrowserManager()
    network_tracker = NetworkTracker()
    page_parser = PageParser()
    report_writer = DocxGenerator()

    # 타임스탬프로 파일명 생성 (예: report_20231025_120000.docx)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_filename = f"capture_{timestamp}.png"
    report_filename = os.path.join(config.OUTPUT_DIR, f"report_{timestamp}.docx")

    try:
        # 1. 브라우저 실행
        page = browser_mgr.launch_browser()

        # 2. 네트워크 추적 시작
        network_tracker.start_tracing(page)

        # 3. 사이트 접속 및 로딩 대기
        browser_mgr.navigate_to(config.TARGET_URL)

        # 4. 화면 캡처
        screenshot_path = browser_mgr.capture_screen(screenshot_filename)

        # [추가됨] 4-1. 상호작용 요소 정밀 분석
        print("[Main] Extracting interactive elements (Buttons/Links)...")
        interactive_data = browser_mgr.extract_interactive_elements()

        # 5. HTML 추출 및 분석
        print("[Main] Analyzing page structure...")
        html_source = browser_mgr.get_html_source()
        analysis_result = page_parser.parse_page(html_source, config.TARGET_URL)

        # 6. 네트워크 로그 회수
        api_logs = network_tracker.get_api_summary()


        report_writer.save_file(report_filename)
        # 7. 보고서 작성
        print("[Main] Generating report...")
        report_writer.create_report(
            url=config.TARGET_URL,
            screenshot_path=screenshot_path,
            page_data=analysis_result,
            api_logs=api_logs,
            interactive_elements = interactive_data  # 데이터 전달
        )
        report_writer.save_file(report_filename)

        print("\n" + "=" * 50)
        print(f"✅ 모든 작업 완료!")
        print(f"📄 보고서 위치: {report_filename}")
        print("=" * 50)

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # 브라우저 종료
        browser_mgr.close()
    input("\n엔터 키를 누르면 프로그램이 종료됩니다...")

if __name__ == "__main__":
    main()