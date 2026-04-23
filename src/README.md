# Web Analysis Report Tool

## Overview

This Python-based tool automates the process of analyzing websites and generating comprehensive reports. It leverages various libraries such as Playwright, BeautifulSoup, and python-docx to extract information about a website's structure, functionality, network activity, and server information.

## Features

### Core Analysis
-   **Automated Browser Interaction:** Uses Playwright to launch a browser, navigate to specified URLs, handle logins, and capture full-page screenshots.
-   **Comprehensive Network Traffic Analysis:** Tracks ALL network requests (API calls, images, CSS, JS, fonts, media, websockets) using Playwright's built-in network interception.
-   **HTML Structure Parsing:** Employs BeautifulSoup to parse HTML source code and extract key elements like titles, meta descriptions, links, and input fields.
-   **Interactive Element Detection:** Identifies and captures screenshots of interactive elements like buttons and links, along with their associated actions.
-   **Login Handling:** Supports websites that require login by automating the navigation and allowing the user to manually complete the login process in a non-headless browser.
-   **Lazy Loading Handling:** Implements smooth scrolling to ensure that all content, including lazy-loaded images, are captured in screenshots.

### OSINT (Open Source Intelligence)
-   **IP WHOIS Analysis:** Performs WHOIS lookups on ALL server IPs to gather ownership and geographic information.
-   **Domain WHOIS:** Extracts registrar, creation/expiration dates, organization, and name servers.
-   **DNS Records:** Queries A, MX, TXT, and NS records for comprehensive DNS analysis.
-   **SSL/TLS Certificate Analysis:** Extracts certificate issuer, validity period, and Subject Alternative Names.
-   **Technology Stack Detection:** Identifies frameworks (React, Vue, Angular), CMS (WordPress, Shopify), analytics tools, and programming languages.
-   **Contact Information Extraction:** Finds emails, phone numbers, and physical addresses from page content.

### Advanced SNS Analysis (NEW!)
-   **18+ Platform Support:** Facebook, Twitter/X, Instagram, LinkedIn, YouTube, TikTok, Telegram, Discord, Reddit, GitHub, Medium, Pinterest, Twitch, VK, WhatsApp, WeChat, KakaoTalk, Line
-   **Username Extraction:** Automatically parses usernames/handles from URLs
-   **Link Validation:** Checks if social media links are active (HTTP status)
-   **Profile Metadata:** Fetches public profile information (followers, bio, etc.)
-   **Context Detection:** Identifies where links appear (header, footer, contact section)
-   **Open Graph & Twitter Card Parsing:** Extracts social media metadata tags
-   **Presence Scoring:** Calculates social media presence score (0-10)
-   **Detailed Reporting:** Comprehensive SNS analysis with validation status and profile details

### Reporting
-   **Customizable DOCX Reports:** Generates well-formatted reports with 10 comprehensive sections including screenshots, tables, and descriptive text.

## Modules

-   `browser_handler.py`: Manages browser launching, navigation, screenshot capturing, and interactive element extraction using Playwright.
-   `network_sniffer.py`: Tracks and summarizes ALL network traffic (including images, CSS, JS, etc.) using Playwright's request and response events.
-   `page_analyzer.py`: Parses HTML content using BeautifulSoup to extract information about page structure and functionality.
-   `report_writer.py`: Generates comprehensive DOCX reports with 10 sections using python-docx.
-   `whois_analyzer.py`: Analyzes IP addresses from network logs to extract WHOIS information.
-   `osint_analyzer.py`: Performs domain WHOIS, DNS, SSL certificate analysis, and technology detection.
-   `sns_analyzer.py`: **NEW!** Deep social media analysis with 18+ platform support, link validation, and profile metadata extraction.
-   `config.py`: Contains configurable parameters such as target URL, output directories, browser settings, and SNS analysis options.
-   `test.py`: Main script to coordinate the analysis process and generate the final report.

## Dependencies

-   playwright
-   beautifulsoup4
-   python-docx
-   ipwhois
-   requests
-   python-whois
-   dnspython

Install all dependencies using pip:

```bash
pip install -r requirements.txt
```

You also need to install the Playwright browser binaries:

```bash
playwright install chromium
```

For detailed installation instructions, see [INSTALL.md](../INSTALL.md)

## Setup for Executable Distribution (PyInstaller)

If you plan to distribute the tool as a standalone executable using PyInstaller, follow these steps:

1.  **Install PyInstaller:**

    ```bash
    pip install pyinstaller
    ```

2.  **Configure Browser Path:** Ensure that the `browser_handler.py` module correctly locates the Chrome executable within the PyInstaller bundle.  The tool expects the Chrome executable to be located under `chrome-win64/chrome.exe` inside the extracted folder.
3.  **Create the Executable:**

    ```bash
    pyinstaller --onefile test.py --add-data "chrome-win64;chrome-win64"
    ```

    Adjust the `--add-data` parameter if the chrome executable is located elsewhere in your PyInstaller distribution.
    The `--onefile` option creates a single executable file, making distribution easier.  Without this option, PyInstaller will create a directory containing the executable file along with all of its dependencies.
4.  **Run the Executable:** The executable will be located in the `dist` directory.

## Usage

1.  **Clone the Repository:**

    ```bash
    git clone <repository_url>
    cd WebAnalysisReport
    ```

2.  **Run the Main Script:**

    ```bash
    python test.py
    ```

3.  **Follow Prompts:** The script will prompt you for the target URL and whether the site requires login. If login is required, the browser will launch in non-headless mode to allow manual login. After login, press Enter in the console to continue the analysis.

## Configuration

Edit the `config.py` file to customize the following settings:

-   `TARGET_URL`: The default URL to analyze.
-   `OUTPUT_DIR`: The directory where reports and screenshots will be saved.
-   `HEADLESS_MODE`: Whether to run the browser in headless mode.
-   `VIEWPORT_SIZE`: The browser's viewport size.
-   `USER_AGENT`:  The browser's user agent string.

## Notes

-   This tool is intended for ethical web analysis and reporting.
-   Be mindful of website terms of service and robots.txt guidelines.
-   The accuracy of the analysis depends on the structure and technologies used by the target website.

---

# 웹 분석 보고서 도구 (Web Analysis Report Tool)

## 개요

이 Python 기반 도구는 웹사이트 분석 및 종합적인 보고서 생성 과정을 자동화합니다. Playwright, BeautifulSoup, python-docx와 같은 다양한 라이브러리를 활용하여 웹사이트의 구조, 기능, 네트워크 활동 및 서버 정보에 대한 데이터를 추출합니다.

## 주요 기능

-   **자동화된 브라우저 상호작용:** Playwright를 사용하여 브라우저를 실행하고, 지정된 URL로 이동하며, 로그인을 처리하고, 전체 화면 스크린샷을 캡처합니다.
-   **네트워크 트래픽 분석:** Playwright에 내장된 네트워크 가로채기 기능을 사용하여 네트워크 요청(API 호출, 리소스 등)을 추적합니다.
-   **HTML 구조 파싱:** BeautifulSoup을 사용하여 HTML 소스 코드를 파싱하고 제목, 메타 설명, 링크, 입력 필드 등 주요 요소를 추출합니다.
-   **상호작용 요소 감지:** 버튼, 링크 등 클릭 가능한 상호작용 요소를 식별하고 관련 동작 정보와 함께 스크린샷을 캡처합니다.
-   **WHOIS 분석:** 네트워크 로그에서 수집된 서버 IP에 대해 WHOIS 조회를 수행하여 소유자 및 지리적 정보를 수집합니다.
-   **보고서 자동 생성:** python-docx를 활용하여 스크린샷, 표, 설명 텍스트가 포함된 서식이 지정된 DOCX 보고서를 생성합니다.
-   **로그인 지원:** 로그인이 필요한 웹사이트의 경우, 헤드리스 모드를 해제하여 사용자가 브라우저 창에서 수동으로 로그인을 완료할 수 있도록 지원합니다.
-   **지연 로딩(Lazy Loading) 처리:** 부드러운 스크롤 기능을 구현하여 지연 로딩되는 이미지를 포함한 모든 콘텐츠가 스크린샷에 캡처되도록 합니다.

## 모듈

-   `browser_handler.py`: Playwright를 사용하여 브라우저 실행, 탐색, 스크린샷 캡처 및 상호작용 요소 추출을 담당합니다.
-   `network_sniffer.py`: Playwright의 요청(Request) 및 응답(Response) 이벤트를 사용하여 네트워크 트래픽을 추적하고 요약합니다.
-   `page_analyzer.py`: BeautifulSoup으로 HTML 콘텐츠를 파싱하여 페이지 구조 및 기능 정보를 추출합니다.
-   `report_writer.py`: 다른 모듈에서 수집한 데이터를 통합하여 python-docx로 DOCX 보고서를 생성합니다.
-   `whois_analyzer.py`: 네트워크 로그의 IP 주소를 분석하여 WHOIS 정보를 추출합니다.
-   `config.py`: 대상 URL, 출력 디렉토리, 브라우저 설정 등 구성 가능한 매개변수를 포함합니다.
-   `test.py`: 분석 과정을 조정하고 최종 보고서를 생성하는 메인 스크립트입니다.

## 의존성 (Dependencies)

-   playwright
-   beautifulsoup4
-   python-docx
-   ipwhois

pip를 사용하여 의존성 패키지를 설치하세요:

```bash
pip install playwright beautifulsoup4 python-docx ipwhois
```

Playwright 브라우저 바이너리도 설치해야 합니다:

```bash
playwright install
```

## 실행 파일 배포를 위한 설정 (PyInstaller)

이 도구를 PyInstaller를 사용하여 독립 실행형 파일(EXE)로 배포하려면 다음 단계를 따르세요:

1.  **PyInstaller 설치:**

    ```bash
    pip install pyinstaller
    ```

2.  **브라우저 경로 설정:** `browser_handler.py` 모듈이 PyInstaller 번들 내에서 Chrome 실행 파일을 올바르게 찾을 수 있는지 확인하세요. 이 도구는 압축 해제된 폴더 내부의 `chrome-win64/chrome.exe` 경로에 Chrome 실행 파일이 위치할 것으로 예상합니다.
3.  **실행 파일 생성:**

    ```bash
    pyinstaller --onefile test.py --add-data "chrome-win64;chrome-win64"
    ```

    PyInstaller 배포판에서 chrome 실행 파일이 다른 곳에 있는 경우 `--add-data` 매개변수를 조정하세요.
    `--onefile` 옵션은 단일 실행 파일을 생성하여 배포를 용이하게 합니다. 이 옵션을 사용하지 않으면 PyInstaller는 모든 의존성 패키지와 함께 실행 파일을 포함하는 디렉토리를 생성합니다.
4.  **실행 파일 실행:** 생성된 실행 파일은 `dist` 폴더에 위치합니다.

## 사용법

1.  **저장소 클론:**

    ```bash
    git clone <repository_url>
    cd WebAnalysisReport
    ```

2.  **메인 스크립트 실행:**

    ```bash
    python test.py
    ```

3.  **프롬프트 지시 따르기:** 스크립트가 실행되면 대상 URL과 로그인이 필요한 사이트인지 묻습니다. 로그인이 필요한 경우 브라우저가 화면에 표시되는 모드(non-headless)로 실행되어 수동으로 로그인할 수 있습니다. 로그인 완료 후 콘솔에서 Enter 키를 누르면 분석이 계속 진행됩니다.

## 설정 (Configuration)

`config.py` 파일을 편집하여 다음 설정을 사용자 지정할 수 있습니다:

-   `TARGET_URL`: 분석할 기본 URL.
-   `OUTPUT_DIR`: 보고서 및 스크린샷이 저장될 디렉토리.
-   `HEADLESS_MODE`: 브라우저를 헤드리스 모드(화면 숨김)로 실행할지 여부.
-   `VIEWPORT_SIZE`: 브라우저의 화면(Viewport) 크기.
-   `USER_AGENT`: 브라우저의 User-Agent 문자열.

## 참고 사항

-   이 도구는 윤리적인 웹 분석 및 보고 목적으로 제작되었습니다.
-   웹사이트의 서비스 약관(Terms of Service) 및 `robots.txt` 가이드라인을 준수하시기 바랍니다.
-   분석의 정확성은 대상 웹사이트의 구조와 사용된 기술에 따라 달라질 수 있습니다.
