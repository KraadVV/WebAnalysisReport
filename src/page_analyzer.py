# src/page_analyzer.py
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class PageParser:
    def __init__(self):
        self.soup = None
        self.summary = {}

    def parse_page(self, html_content, base_url):
        """
        HTML 소스를 받아 BeautifulSoup 객체로 변환하고 분석을 수행합니다.
        """
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.base_url_domain = urlparse(base_url).netloc

        # 분석 실행
        self.summary = {
            "title": self._get_title(),
            "meta_description": self._get_meta_desc(),
            "inputs": self._analyze_inputs(),
            "links": self._analyze_links(),
            "buttons": self._analyze_buttons(),
            "guessed_features": self._guess_features()
        }
        return self.summary

    def _get_title(self):
        return self.soup.title.string.strip() if self.soup.title else "No Title"

    def _get_meta_desc(self):
        meta = self.soup.find("meta", attrs={"name": "description"})
        return meta["content"] if meta else "No Description"

    def _analyze_inputs(self):
        """입력 필드(Input) 분석"""
        inputs = self.soup.find_all("input")
        input_summary = []
        for i in inputs:
            # 숨겨진 필드는 제외하고 사용자에게 보이는 것만 기록
            if i.get("type") != "hidden":
                input_summary.append({
                    "type": i.get("type", "text"),
                    "name": i.get("name", ""),
                    "placeholder": i.get("placeholder", "")
                })
        return input_summary

    def _analyze_links(self):
        """링크(A 태그) 분석: 내부/외부 링크 구분"""
        links = self.soup.find_all("a", href=True)
        internal = 0
        external = 0

        for link in links:
            href = link['href']
            # 도메인이 같거나 상대 경로(/path)면 내부 링크
            if self.base_url_domain in href or href.startswith("/"):
                internal += 1
            elif href.startswith("http"):
                external += 1

        return {"total": len(links), "internal": internal, "external": external}

    def _analyze_buttons(self):
        """버튼 요소 분석"""
        buttons = self.soup.find_all("button")
        # type="submit"은 폼 제출용, 그 외는 일반 기능용
        submit_btns = sum(1 for b in buttons if b.get("type") == "submit")
        return {"total": len(buttons), "submit_type": submit_btns, "others": len(buttons) - submit_btns}

    def _guess_features(self):
        """
        HTML 구조를 단서로 사이트의 기능을 추측합니다 (Heuristics).
        """
        features = []
        html_str = str(self.soup).lower()

        # 1. 로그인 기능 감지 (비밀번호 입력창 존재 여부)
        if self.soup.find("input", {"type": "password"}):
            features.append("로그인 (Login)")

        # 2. 회원가입 기능 감지 (키워드 매칭)
        if "sign up" in html_str or "register" in html_str or "회원가입" in html_str:
            features.append("회원가입 (Sign Up)")

        # 3. 검색 기능 감지
        if self.soup.find("input", {"type": "search"}) or "search" in html_str:
            features.append("검색 (Search)")

        # 4. 장바구니/커머스 감지
        if "cart" in html_str or "장바구니" in html_str or "checkout" in html_str:
            features.append("쇼핑/장바구니 (E-commerce)")

        return features if features else ["특수 기능 감지되지 않음"]