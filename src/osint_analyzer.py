# src/osint_analyzer.py
import re
import socket
import ssl
import whois
import dns.resolver
from urllib.parse import urlparse
from datetime import datetime


class OSINTAnalyzer:
    def __init__(self):
        self.domain = None
        self.url = None
    
    def analyze_domain(self, url):
        """
        도메인에 대한 종합적인 OSINT 분석을 수행합니다.
        """
        self.url = url
        parsed = urlparse(url)
        self.domain = parsed.netloc
        
        print(f"[OSINT] Analyzing domain: {self.domain}")
        
        results = {
            'domain': self.domain,
            'whois': self._get_whois_info(),
            'dns': self._get_dns_records(),
            'server_ips': self.get_server_ip_nslookup(),  # nslookup으로 실제 서버 IP 조회
            'ssl': self._get_ssl_info(url),
            'contacts': {},
            'technologies': {}
        }
        
        return results
    
    def _get_whois_info(self):
        """WHOIS 정보를 조회합니다."""
        print(f"[OSINT] Fetching WHOIS information...")
        try:
            w = whois.whois(self.domain)
            
            # 날짜 처리 (리스트일 수 있음)
            creation_date = w.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            
            expiration_date = w.expiration_date
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]
            
            # 이름 서버 처리
            name_servers = w.name_servers
            if isinstance(name_servers, list):
                name_servers = name_servers[:5]  # 최대 5개만
            
            return {
                'registrar': str(w.registrar) if w.registrar else 'N/A',
                'creation_date': str(creation_date) if creation_date else 'N/A',
                'expiration_date': str(expiration_date) if expiration_date else 'N/A',
                'name_servers': name_servers if name_servers else [],
                'org': str(w.org) if w.org else 'N/A',
                'emails': w.emails if w.emails else []
            }
        except Exception as e:
            print(f"[OSINT] WHOIS lookup failed: {e}")
            return {
                'registrar': 'Lookup Failed',
                'creation_date': 'N/A',
                'expiration_date': 'N/A',
                'name_servers': [],
                'org': 'N/A',
                'emails': []
            }
    
    def get_server_ip_nslookup(self):
        """
        nslookup 명령어를 사용하여 실제 서버 IP 주소를 조회합니다.
        DNS 서버 IP가 아닌 대상 도메인의 실제 서버 IP를 반환합니다.
        """
        import subprocess
        import re
        
        try:
            print(f"[OSINT] Running nslookup for {self.domain}...")
            
            # nslookup 명령 실행
            result = subprocess.run(
                ['nslookup', self.domain], 
                capture_output=True, 
                text=True, 
                timeout=10,
                shell=True  # Windows에서 필요할 수 있음
            )
            
            # 출력 파싱하여 IP 주소 추출
            lines = result.stdout.split('\n')
            server_ips = []
            
            # "Name:" 라인 이후의 "Address:" 라인에서 IP 찾기
            found_name = False
            for line in lines:
                # 도메인 이름이 포함된 Name: 라인 찾기
                if 'Name:' in line or '이름:' in line:
                    if self.domain in line:
                        found_name = True
                # Name 라인 이후의 Address 라인에서 IP 추출
                elif found_name and ('Address:' in line or '주소:' in line or 'Addresses:' in line):
                    # IP 주소 패턴 매칭
                    ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                    if ip_match:
                        ip = ip_match.group(1)
                        # DNS 서버 IP 제외 (보통 127.x.x.x나 192.168.x.x가 아닌 공인 IP)
                        if not ip.startswith('127.') and ip not in server_ips:
                            server_ips.append(ip)
                            print(f"[OSINT] ✓ Found server IP: {ip}")
            
            # 대체 방법: socket 라이브러리 사용
            if not server_ips:
                print(f"[OSINT] nslookup parsing failed, trying socket.gethostbyname()...")
                import socket
                try:
                    ip = socket.gethostbyname(self.domain)
                    server_ips.append(ip)
                    print(f"[OSINT] ✓ Found server IP (via socket): {ip}")
                except Exception as e:
                    print(f"[OSINT] socket.gethostbyname() failed: {e}")
            
            return server_ips
            
        except subprocess.TimeoutExpired:
            print(f"[OSINT] nslookup timeout for {self.domain}")
            return []
        except FileNotFoundError:
            print(f"[OSINT] nslookup command not found, trying socket fallback...")
            # nslookup이 없는 경우 socket 사용
            import socket
            try:
                ip = socket.gethostbyname(self.domain)
                print(f"[OSINT] ✓ Found server IP (via socket): {ip}")
                return [ip]
            except Exception as e:
                print(f"[OSINT] socket.gethostbyname() failed: {e}")
                return []
        except Exception as e:
            print(f"[OSINT] nslookup failed: {e}")
            return []
    
    def _get_dns_records(self):
        """DNS 레코드를 조회합니다."""
        print(f"[OSINT] Fetching DNS records...")
        dns_info = {
            'A': [],
            'MX': [],
            'TXT': [],
            'NS': []
        }
        
        record_types = ['A', 'MX', 'TXT', 'NS']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(self.domain, record_type)
                for rdata in answers:
                    if record_type == 'MX':
                        dns_info[record_type].append(str(rdata.exchange))
                    else:
                        dns_info[record_type].append(str(rdata))
            except Exception as e:
                # 레코드가 없거나 조회 실패
                pass
        
        return dns_info
    
    def _get_ssl_info(self, url):
        """SSL/TLS 인증서 정보를 조회합니다."""
        print(f"[OSINT] Fetching SSL certificate information...")
        
        if not url.startswith('https'):
            return {'available': False, 'reason': 'Not HTTPS'}
        
        try:
            parsed = urlparse(url)
            hostname = parsed.netloc
            port = 443
            
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Subject 정보 추출
                    subject = dict(x[0] for x in cert['subject'])
                    issuer = dict(x[0] for x in cert['issuer'])
                    
                    # SANs (Subject Alternative Names)
                    san_list = []
                    if 'subjectAltName' in cert:
                        san_list = [x[1] for x in cert['subjectAltName']]
                    
                    return {
                        'available': True,
                        'issuer': issuer.get('organizationName', 'N/A'),
                        'subject': subject.get('commonName', 'N/A'),
                        'valid_from': cert.get('notBefore', 'N/A'),
                        'valid_until': cert.get('notAfter', 'N/A'),
                        'san': san_list[:10]  # 최대 10개
                    }
        except Exception as e:
            print(f"[OSINT] SSL lookup failed: {e}")
            return {
                'available': False,
                'reason': str(e)
            }
    
    def extract_contacts_from_html(self, html_content):
        """
        HTML에서 연락처 정보를 추출합니다.
        """
        print("[OSINT] Extracting contact information from HTML...")
        
        contacts = {
            'emails': [],
            'phones': [],
            'social_media': {}
        }
        
        # 이메일 추출
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, html_content)
        contacts['emails'] = list(set(emails))[:10]  # 중복 제거, 최대 10개
        
        # 전화번호 추출 (한국, 국제 형식)
        phone_patterns = [
            r'\b\d{2,3}-\d{3,4}-\d{4}\b',  # 한국 형식: 02-1234-5678
            r'\b\d{3}-\d{4}-\d{4}\b',      # 010-1234-5678
            r'\+\d{1,3}\s?\d{1,4}\s?\d{1,4}\s?\d{1,4}',  # 국제 형식
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, html_content)
            contacts['phones'].extend(phones)
        
        contacts['phones'] = list(set(contacts['phones']))[:10]
        
        # 소셜 미디어 링크 추출
        social_platforms = {
            'facebook': r'(?:https?://)?(?:www\.)?facebook\.com/[\w\-\.]+',
            'twitter': r'(?:https?://)?(?:www\.)?twitter\.com/[\w\-\.]+',
            'linkedin': r'(?:https?://)?(?:www\.)?linkedin\.com/(?:in|company)/[\w\-\.]+',
            'instagram': r'(?:https?://)?(?:www\.)?instagram\.com/[\w\-\.]+',
            'youtube': r'(?:https?://)?(?:www\.)?youtube\.com/(?:c|channel|user)/[\w\-\.]+',
            'github': r'(?:https?://)?(?:www\.)?github\.com/[\w\-\.]+',
        }
        
        for platform, pattern in social_platforms.items():
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                contacts['social_media'][platform] = list(set(matches))[:3]
        
        return contacts
    
    def detect_technologies(self, html_content, response_headers=None):
        """
        웹사이트에서 사용된 기술 스택을 감지합니다.
        """
        print("[OSINT] Detecting technologies...")
        
        technologies = {
            'frameworks': [],
            'cms': [],
            'analytics': [],
            'server': 'Unknown',
            'programming_language': []
        }
        
        html_lower = html_content.lower()
        
        # 프레임워크 감지
        framework_signatures = {
            'React': ['react', '_react', 'reactdom'],
            'Vue.js': ['vue.js', 'vue.min.js', '__vue__'],
            'Angular': ['ng-app', 'ng-controller', 'angular.js'],
            'jQuery': ['jquery', 'jquery.min.js'],
            'Bootstrap': ['bootstrap.css', 'bootstrap.min.css'],
            'Next.js': ['__next', '_next/static'],
            'Nuxt.js': ['__nuxt', '_nuxt/'],
        }
        
        for tech, signatures in framework_signatures.items():
            if any(sig in html_lower for sig in signatures):
                technologies['frameworks'].append(tech)
        
        # CMS 감지
        cms_signatures = {
            'WordPress': ['wp-content', 'wp-includes', 'wordpress'],
            'Drupal': ['drupal', '/sites/default/'],
            'Joomla': ['joomla', '/components/com_'],
            'Shopify': ['shopify', 'cdn.shopify.com'],
            'Wix': ['wix.com', 'parastorage.com'],
        }
        
        for cms, signatures in cms_signatures.items():
            if any(sig in html_lower for sig in signatures):
                technologies['cms'].append(cms)
        
        # 분석 도구 감지
        analytics_signatures = {
            'Google Analytics': ['google-analytics.com', 'gtag', 'ga.js'],
            'Google Tag Manager': ['googletagmanager.com', 'gtm.js'],
            'Facebook Pixel': ['facebook.net/en_us/fbevents.js', 'fbq('],
            'Hotjar': ['hotjar.com'],
            'Mixpanel': ['mixpanel.com'],
        }
        
        for tool, signatures in analytics_signatures.items():
            if any(sig in html_lower for sig in signatures):
                technologies['analytics'].append(tool)
        
        # 서버 정보 (헤더에서)
        if response_headers:
            server = response_headers.get('server', 'Unknown')
            technologies['server'] = server
        
        # 프로그래밍 언어 추측
        if '.php' in html_lower or 'php' in html_lower:
            technologies['programming_language'].append('PHP')
        if '.asp' in html_lower or '.aspx' in html_lower:
            technologies['programming_language'].append('ASP.NET')
        if '.jsp' in html_lower:
            technologies['programming_language'].append('Java/JSP')
        
        return technologies
