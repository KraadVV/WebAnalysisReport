# src/network_sniffer.py
import socket
from urllib.parse import urlparse


class NetworkTracker:
    def __init__(self):
        self.api_logs = []  # 수집된 API 정보를 저장할 리스트
        self.all_resources = []  # 모든 리소스 (이미지, CSS, JS 등 포함)

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
        parsed_url = urlparse(request.url)
        domain = parsed_url.netloc

        # 도메인 -> IP 변환
        ip_address = self._resolve_ip(domain)

        # 모든 리소스 기록
        resource_entry = {
            "url": request.url,
            "method": request.method,
            "type": request.resource_type,
            "domain": domain,
            "ip": ip_address,
            "status": "Pending"
        }
        self.all_resources.append(resource_entry)

        # API 관련 요청만 별도로 기록 (기존 기능 유지)
        target_types = ["xhr", "fetch", "document"]
        if request.resource_type in target_types:
            self.api_logs.append(resource_entry)

    def _handle_response(self, response):
        """응답(Response)을 가로채서 상태 코드를 업데이트합니다."""
        # 모든 리소스 업데이트
        for resource in self.all_resources:
            if resource["url"] == response.request.url:
                resource["status"] = response.status
                break
        
        # API 로그도 업데이트
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

    def get_all_resources(self):
        """모든 네트워크 리소스를 반환합니다."""
        return self.all_resources
    
    def get_unique_ips(self):
        """중복 제거된 모든 IP 주소 목록을 반환합니다."""
        unique_ips = {}
        for resource in self.all_resources:
            ip = resource.get('ip')
            if ip and ip != 'Unknown IP':
                if ip not in unique_ips:
                    unique_ips[ip] = {
                        'ip': ip,
                        'domain': resource.get('domain'),
                        'types': set(),
                        'count': 0
                    }
                unique_ips[ip]['types'].add(resource.get('type'))
                unique_ips[ip]['count'] += 1
        
        # Set을 리스트로 변환
        for ip_data in unique_ips.values():
            ip_data['types'] = list(ip_data['types'])
        
        return list(unique_ips.values())

    def get_resource_summary(self):
        """리소스 타입별 통계를 반환합니다."""
        summary = {}
        for resource in self.all_resources:
            res_type = resource.get('type', 'unknown')
            if res_type not in summary:
                summary[res_type] = 0
            summary[res_type] += 1
        return summary

    def clear_logs(self):
        """로그를 초기화합니다."""
        self.api_logs = []
        self.all_resources = []
