# src/whois_analyzer.py
from ipwhois import IPWhois
import time


class WhoisAnalyzer:
    def __init__(self):
        pass

    def analyze_ips(self, api_logs):
        """
        API 로그에서 수집된 IP들의 WHOIS 정보를 조회합니다.
        중복된 IP는 제거하고 조회합니다.
        """
        print("[Whois] Starting WHOIS lookup for detected IPs...")

        # 1. 중복 IP 제거 및 유효성 검사
        unique_ips = set()
        for log in api_logs:
            ip = log.get('ip')
            # IP가 없거나, 분석 실패('Unknown'), 혹은 로컬호스트 등은 제외
            if ip and ip not in ['-', 'Unknown IP', '127.0.0.1'] and not ip.startswith('192.168.'):
                unique_ips.add(ip)

        results = []
        total = len(unique_ips)

        print(f"[Whois] Found {total} unique IPs. (This might take a while...)")

        for idx, ip in enumerate(unique_ips):
            try:
                # 진행 상황 표시 (너무 오래 걸리면 답답하니까)
                print(f"[Whois] Looking up ({idx + 1}/{total}): {ip}")

                # RDAP 프로토콜을 사용해 조회 (가장 빠르고 정확함)
                obj = IPWhois(ip)
                res = obj.lookup_rdap(depth=1)  # depth=1로 상세 정보 최소화하여 속도 향상

                # 필요한 정보만 추출
                network = res.get('network', {})
                if network is None: network = {}


                asn_desc = res.get('asn_description', 'N/A')  # ISP/기업명
                org_name = network.get('name')
                final_org = (asn_desc or org_name or 'N/A')

                country = network.get('country') or 'N/A'  # 국가 코드
                cidr = network.get('cidr', 'N/A')  # IP 대역

                results.append({
                    "ip": ip,
                    "org": str(final_org),  # ISP 이름 우선 사용
                    "country": str(country),
                    "cidr": str(cidr)
                })

                # 차단 방지를 위한 약간의 딜레이
                time.sleep(0.5)

            except Exception as e:
                print(f"[Whois] Failed lookup for {ip}: {e}")
                results.append({
                    "ip": ip,
                    "org": "Lookup Failed",
                    "country": "-",
                    "cidr": "-"
                })

        return results