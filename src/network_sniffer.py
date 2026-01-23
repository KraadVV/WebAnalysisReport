# src/network_sniffer.py
import socket
from urllib.parse import urlparse


class NetworkTracker:
    def __init__(self):
        self.api_logs = []  # 수집된 API 정보를 저장할 리스트

    def start_tracing(self, page):
        """
        브라우저 페이지에 이벤트 리스너를 등록하여 네트워크 트래픽을 감시합니다.
        """
        print("[Network] Start tracing network traffic...")

        # 요청이 발생했을 때 실행될 함수 등록
        page.on("request", self._handle_request)

        # 응답이 왔을 때 실행될 함수 등록 (상태 코드 확인용)
        page.on("response", self._handle_response)

    def _handle_request(self, request):
        """요청(Request)을 가로채서 분석합니다."""
        # 분석 대상 리소스 타입 필터링
        # xhr/fetch: 비동기 데이터 통신 (API)
        # document: 페이지 자체의 HTML 요청
        target_types = ["xhr", "fetch", "document"]

        if request.resource_type in target_types:
            parsed_url = urlparse(request.url)
            domain = parsed_url.netloc

            # 도메인 -> IP 변환
            ip_address = self._resolve_ip(domain)

            log_entry = {
                "url": request.url,
                "method": request.method,
                "type": request.resource_type,
                "domain": domain,
                "ip": ip_address,
                "status": "Pending"  # 응답 오기 전
            }

            # 리스트에 추가
            self.api_logs.append(log_entry)

    def _handle_response(self, response):
        """응답(Response)을 가로채서 상태 코드를 업데이트합니다."""
        # 기록해둔 요청 리스트에서 해당 URL을 찾아 상태 코드 업데이트
        # (간단한 구현을 위해 URL로 매칭하지만, 실제로는 Request ID로 매칭하는 게 더 정확함)
        for log in self.api_logs:
            if log["url"] == response.request.url:
                log["status"] = response.status
                break

    def _resolve_ip(self, domain):
        """도메인 주소를 입력받아 IP 주소를 반환합니다."""
        try:
            # 포트 번호가 있다면 제거 (예: google.com:443 -> google.com)
            if ":" in domain:
                domain = domain.split(":")[0]
            return socket.gethostbyname(domain)
        except Exception:
            return "Unknown IP"

    def get_api_summary(self):
        """수집된 API 로그를 반환합니다."""
        return self.api_logs

    def clear_logs(self):
        """로그를 초기화합니다."""
        self.api_logs = []