# 🔍 Web Analysis Report Tool

> Automated web intelligence gathering and comprehensive OSINT reporting tool

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Playwright](https://img.shields.io/badge/playwright-enabled-brightgreen.svg)](https://playwright.dev/)

A powerful Python-based tool that automates website analysis and generates comprehensive intelligence reports. Leverages Playwright for browser automation, performs deep OSINT analysis, tracks network activity, and extracts social media intelligence across 18+ platforms.

---

## ✨ Key Features

### 🎯 Core Analysis
- **Automated Browser Interaction** - Playwright-powered navigation, login handling, and screenshot capture
- **Comprehensive Network Tracking** - Monitors ALL resources (API calls, images, CSS, JS, fonts, media, WebSockets)
- **HTML Structure Parsing** - Extracts titles, meta tags, links, forms, and interactive elements
- **Interactive Element Detection** - Identifies and captures buttons, links with action information
- **Lazy Loading Support** - Smart scrolling to capture dynamically loaded content

### 🔐 OSINT Intelligence
- **Domain WHOIS Analysis** - Registrar, creation/expiration dates, organization, name servers
- **DNS Records** - A, MX, TXT, NS record queries
- **SSL/TLS Certificate Analysis** - Issuer, validity period, Subject Alternative Names
- **Technology Stack Detection** - Identifies frameworks (React, Vue, Angular), CMS (WordPress, Shopify), analytics tools
- **Contact Extraction** - Emails, phone numbers, physical addresses
- **IP WHOIS Lookups** - Geographic and ownership information for all contacted servers

### 📱 Advanced SNS Analysis
- **18+ Platform Support** - Facebook, Twitter/X, Instagram, LinkedIn, YouTube, TikTok, Telegram, Discord, Reddit, GitHub, Medium, Pinterest, Twitch, VK, WhatsApp, WeChat, KakaoTalk, Line
- **Username Extraction** - Automatically parses handles from all URL formats
- **Link Validation** - HTTP status checking for discovered links
- **Profile Metadata** - Fetches public profile information (Open Graph, Twitter Cards)
- **Context Detection** - Identifies link placement (header, footer, social section)
- **Presence Scoring** - Calculates 0-10 social media presence score

### 🌐 Smart Chrome Detection (NEW!)
- **Auto-Detection** - Finds Chrome via Windows Registry and common paths
- **Interactive Prompts** - User-friendly fallback options when Chrome not found
- **Config Persistence** - Remembers user preferences in `user_config.json`
- **Flexible** - Supports custom Chrome installations and portable versions
- **Safe Fallback** - Always falls back to Playwright's bundled Chromium

### 📊 Professional Reporting
- **DOCX Reports** - Well-formatted reports with 10 comprehensive sections
- **Screenshots** - Full-page captures and individual element screenshots
- **Tables & Charts** - Organized data presentation
- **Bilingual Support** - English and Korean documentation

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/KraadVV/WebAnalysisReport.git
   cd WebAnalysisReport
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

For detailed installation instructions, see **[INSTALL.md](INSTALL.md)**

### Basic Usage

```bash
python test.py
```

The tool will prompt you for:
- Target URL to analyze
- Whether the site requires login (optional)

**Example:**
```
Enter the URL to analyze: https://example.com
Does this site require login? (y/n): n

[Browser] Launching browser...
[Browser] Auto-detecting Chrome installation...
[Browser] ✓ Found Chrome via Windows Registry
[Browser] Navigating to: https://example.com
...
```

Reports are saved to the `outputs/` directory.

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[INSTALL.md](INSTALL.md)** | Detailed installation and setup guide |
| **[CHROME_DETECTION.md](CHROME_DETECTION.md)** | Chrome auto-detection feature guide |
| **[SNS_FEATURES.md](SNS_FEATURES.md)** | Social media analysis capabilities |
| **[CHANGELOG.md](CHANGELOG.md)** | Version history and updates |
| **[src/README.md](src/README.md)** | Developer documentation for source code |

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Target URL
TARGET_URL = "https://www.google.com"

# Browser Settings
HEADLESS_MODE = True  # Set to False to see browser
VIEWPORT_SIZE = {"width": 1280, "height": 720}

# SNS Analysis
SNS_VALIDATE_LINKS = True
SNS_FETCH_METADATA = True
SNS_MAX_VALIDATE = 20

# Report Optimization
MAX_INTERACTIVE_ELEMENTS = 15
FILTER_LANGUAGE_SELECTORS = True
```

---

## 📦 Project Structure

```
WebAnalysisReport/
├── README.md                    # This file
├── INSTALL.md                   # Installation guide
├── CHANGELOG.md                 # Version history
├── CHROME_DETECTION.md          # Chrome detection docs
├── SNS_FEATURES.md              # SNS analysis docs
├── config.py                    # Configuration file
├── requirements.txt             # Python dependencies
├── test.py                      # Main script
├── src/
│   ├── browser_handler.py       # Browser automation
│   ├── network_sniffer.py       # Network tracking
│   ├── page_analyzer.py         # HTML parsing
│   ├── osint_analyzer.py        # OSINT analysis
│   ├── sns_analyzer.py          # Social media analysis
│   ├── whois_analyzer.py        # IP WHOIS lookups
│   └── report_writer.py         # Report generation
└── outputs/                     # Generated reports
```

---

## 📋 Generated Report Sections

1. **Initial Screen Capture** - Full-page screenshot
2. **Page Structure Analysis** - HTML elements, meta tags, forms
3. **API Communication Analysis** - Network requests and responses
4. **Server IP WHOIS Information** - IP ownership and location
5. **Interactive Elements Analysis** - Buttons, links with screenshots
6. **Network Resource Analysis** - All resources with IP mapping
7. **OSINT Information** - Domain WHOIS, DNS, SSL certificates
8. **Technology Stack** - Detected frameworks and tools
9. **Contact & Social Media** - Extracted contact information
10. **Deep SNS Analysis** - Comprehensive social media intelligence

---

## 🔧 Advanced Features

### Login Support
For sites requiring authentication:
```bash
python test.py
# When prompted:
Does this site require login? (y/n): y
```
The browser will launch in visible mode, allowing manual login before analysis continues.

### Chrome Auto-Detection
The tool automatically finds Chrome on your system:
- ✅ Windows Registry lookup
- ✅ Common installation paths
- ✅ Bundled Chrome (for EXE distribution)
- ✅ User-provided custom paths

If Chrome isn't found, you'll be prompted to either use Playwright's Chromium or provide a custom path. Your choice is saved for future runs.

See **[CHROME_DETECTION.md](CHROME_DETECTION.md)** for details.

### SNS Analysis
Analyzes social media presence across 18+ platforms with:
- Username extraction from URLs
- Link validation (HTTP status)
- Profile metadata fetching
- Presence scoring (0-10)

See **[SNS_FEATURES.md](SNS_FEATURES.md)** for details.

---

## 🛠️ Development

### Module Overview

| Module | Purpose |
|--------|---------|
| `browser_handler.py` | Playwright browser automation, screenshot capture |
| `network_sniffer.py` | Network traffic monitoring and analysis |
| `page_analyzer.py` | HTML parsing with BeautifulSoup |
| `osint_analyzer.py` | WHOIS, DNS, SSL, technology detection |
| `sns_analyzer.py` | Social media intelligence gathering |
| `whois_analyzer.py` | IP address WHOIS lookups |
| `report_writer.py` | DOCX report generation |

### Dependencies

- `playwright` - Browser automation
- `beautifulsoup4` - HTML parsing
- `python-docx` - Report generation
- `ipwhois` - IP WHOIS lookups
- `python-whois` - Domain WHOIS
- `dnspython` - DNS queries
- `requests` - HTTP requests

---

## 📝 Usage Examples

### Basic Analysis
```bash
python test.py
# Enter URL when prompted
```

### With Login
```bash
python test.py
# Choose 'y' for login
# Complete login in browser
# Press Enter to continue
```

### Custom Configuration
```python
# Edit config.py
TARGET_URL = "https://example.com"
HEADLESS_MODE = False  # See browser
SNS_VALIDATE_LINKS = True
```

---

## 🐛 Troubleshooting

### Chrome Not Found
If you see "Chrome not found" warnings:
1. The tool will prompt you for options
2. Choose to use Playwright's Chromium or provide Chrome path
3. Your choice is saved to `user_config.json`

See **[CHROME_DETECTION.md](CHROME_DETECTION.md)** for details.

### Network Issues
- Ensure stable internet connection for WHOIS/DNS lookups
- Some services may rate-limit requests
- The tool gracefully handles failures

### Report Generation
- Reports are saved to `outputs/` directory
- Screenshots in `outputs/screenshots/`
- Check console for error messages

---

## 📜 Version History

### v2.2 (2026-04-23) - Chrome Auto-Detection
- Smart Chrome browser detection system
- Windows Registry lookup
- Interactive user prompts with validation
- Config persistence via `user_config.json`

### v2.1 (2026-04-23) - SNS Intelligence
- 18+ social media platform support
- Username extraction and validation
- Profile metadata fetching
- Presence scoring system

### v2.0 (2026-04-23) - OSINT & Network Analysis
- Comprehensive network resource tracking
- Domain WHOIS, DNS, SSL analysis
- Technology stack detection
- Contact information extraction

See **[CHANGELOG.md](CHANGELOG.md)** for complete history.

---

## ⚠️ Ethical Use

This tool is intended for:
- ✅ Legitimate security research
- ✅ Website analysis and auditing
- ✅ OSINT investigations
- ✅ Educational purposes

Please:
- ⚠️ Respect website terms of service
- ⚠️ Follow robots.txt guidelines
- ⚠️ Obtain proper authorization
- ⚠️ Use responsibly and ethically

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Author

**KraadVV**
- GitHub: [@KraadVV](https://github.com/KraadVV)

---

## 🙏 Acknowledgments

- [Playwright](https://playwright.dev/) - Browser automation
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [python-docx](https://python-docx.readthedocs.io/) - Document generation

---

<div align="center">

**[⬆ Back to Top](#-web-analysis-report-tool)**

Made with ❤️ for the OSINT community

</div>

---

# 🔍 웹 분석 보고서 도구 (Korean)

> 자동화된 웹 인텔리전스 수집 및 종합 OSINT 보고 도구

## 주요 기능

### 🎯 핵심 분석
- **자동화된 브라우저 상호작용** - Playwright 기반 탐색, 로그인 처리, 스크린샷 캡처
- **종합 네트워크 추적** - 모든 리소스 모니터링 (API, 이미지, CSS, JS, 폰트, 미디어, WebSocket)
- **HTML 구조 파싱** - 제목, 메타 태그, 링크, 폼, 상호작용 요소 추출
- **상호작용 요소 감지** - 버튼, 링크 식별 및 동작 정보 캡처
- **지연 로딩 지원** - 동적 로드 콘텐츠 캡처를 위한 스마트 스크롤

### 🔐 OSINT 인텔리전스
- **도메인 WHOIS 분석** - 등록기관, 생성/만료일, 조직, 네임서버
- **DNS 레코드** - A, MX, TXT, NS 레코드 조회
- **SSL/TLS 인증서 분석** - 발급자, 유효 기간, Subject Alternative Names
- **기술 스택 감지** - 프레임워크(React, Vue, Angular), CMS(WordPress, Shopify), 분석 도구 식별
- **연락처 추출** - 이메일, 전화번호, 실제 주소
- **IP WHOIS 조회** - 접속한 모든 서버의 지리적 위치 및 소유권 정보

### 📱 고급 SNS 분석
- **18개 이상 플랫폼 지원** - Facebook, Twitter/X, Instagram, LinkedIn, YouTube, TikTok, Telegram, Discord, Reddit, GitHub, Medium, Pinterest, Twitch, VK, WhatsApp, WeChat, KakaoTalk, Line
- **사용자명 추출** - 모든 URL 형식에서 자동으로 핸들 파싱
- **링크 검증** - 발견된 링크의 HTTP 상태 확인
- **프로필 메타데이터** - 공개 프로필 정보 가져오기 (Open Graph, Twitter Cards)
- **컨텍스트 감지** - 링크 배치 위치 식별 (헤더, 푸터, 소셜 섹션)
- **존재감 점수** - 0-10 소셜 미디어 존재감 점수 계산

### 🌐 스마트 Chrome 감지 (신규!)
- **자동 감지** - Windows 레지스트리 및 일반 경로를 통해 Chrome 찾기
- **대화형 프롬프트** - Chrome을 찾을 수 없을 때 사용자 친화적 대체 옵션
- **설정 지속성** - `user_config.json`에 사용자 기본 설정 저장
- **유연성** - 사용자 정의 Chrome 설치 및 포터블 버전 지원
- **안전한 대체** - 항상 Playwright의 번들 Chromium으로 대체

## 🚀 빠른 시작

### 설치

```bash
git clone https://github.com/KraadVV/WebAnalysisReport.git
cd WebAnalysisReport
pip install -r requirements.txt
playwright install chromium
```

### 사용법

```bash
python test.py
```

자세한 내용은 **[INSTALL.md](INSTALL.md)** 를 참조하세요.

## 📚 문서

- **[INSTALL.md](INSTALL.md)** - 상세 설치 가이드
- **[CHROME_DETECTION.md](CHROME_DETECTION.md)** - Chrome 자동 감지 기능
- **[SNS_FEATURES.md](SNS_FEATURES.md)** - 소셜 미디어 분석 기능
- **[CHANGELOG.md](CHANGELOG.md)** - 버전 히스토리

## ⚙️ 설정

`config.py` 파일을 편집하여 사용자 정의:

```python
TARGET_URL = "https://www.google.com"
HEADLESS_MODE = True  # False로 설정하면 브라우저 표시
SNS_VALIDATE_LINKS = True
MAX_INTERACTIVE_ELEMENTS = 15
```

## 📝 생성되는 보고서 섹션

1. 초기 화면 캡처
2. 페이지 구조 분석
3. API 통신 분석
4. 서버 IP WHOIS 정보
5. 상호작용 요소 분석
6. 네트워크 리소스 분석
7. OSINT 정보
8. 기술 스택
9. 연락처 및 소셜 미디어
10. 심층 SNS 분석

## ⚠️ 윤리적 사용

이 도구는 다음 용도로 사용됩니다:
- ✅ 합법적인 보안 연구
- ✅ 웹사이트 분석 및 감사
- ✅ OSINT 조사
- ✅ 교육 목적

다음을 준수하세요:
- ⚠️ 웹사이트 서비스 약관 존중
- ⚠️ robots.txt 가이드라인 준수
- ⚠️ 적절한 권한 획득
- ⚠️ 책임감 있고 윤리적으로 사용

---

<div align="center">

**[⬆ 맨 위로](#-web-analysis-report-tool)**

OSINT 커뮤니티를 위해 ❤️ 로 제작

</div>
