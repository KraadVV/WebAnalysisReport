# src/sns_analyzer.py
import re
import requests
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import time


class SNSAnalyzer:
    """
    Comprehensive Social Media Network Analysis
    Extracts, validates, and analyzes social media presence
    """
    
    def __init__(self, api_keys=None):
        self.api_keys = api_keys or {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Comprehensive platform patterns
        self.platform_patterns = {
            'facebook': [
                r'(?:https?://)?(?:www\.|m\.)?facebook\.com/(?:profile\.php\?id=\d+|(?:pages/)?[\w\-\.]+/?)',
                r'(?:https?://)?(?:www\.)?fb\.com/[\w\-\.]+'
            ],
            'twitter': [
                r'(?:https?://)?(?:www\.)?twitter\.com/[\w\-]+',
                r'(?:https?://)?(?:www\.)?x\.com/[\w\-]+'
            ],
            'instagram': [
                r'(?:https?://)?(?:www\.)?instagram\.com/[\w\-\.]+'
            ],
            'linkedin': [
                r'(?:https?://)?(?:www\.)?linkedin\.com/(?:in|company)/[\w\-\.]+'
            ],
            'youtube': [
                r'(?:https?://)?(?:www\.)?youtube\.com/(?:c|channel|user|@)[\w\-\.]+',
                r'(?:https?://)?(?:www\.)?youtu\.be/[\w\-]+'
            ],
            'tiktok': [
                r'(?:https?://)?(?:www\.)?tiktok\.com/@[\w\-\.]+'
            ],
            'telegram': [
                r'(?:https?://)?(?:www\.)?t\.me/[\w\-]+',
                r'(?:https?://)?(?:www\.)?telegram\.me/[\w\-]+'
            ],
            'discord': [
                r'(?:https?://)?(?:www\.)?discord\.gg/[\w\-]+',
                r'(?:https?://)?(?:www\.)?discord\.com/invite/[\w\-]+'
            ],
            'reddit': [
                r'(?:https?://)?(?:www\.)?reddit\.com/(?:r|u|user)/[\w\-]+'
            ],
            'github': [
                r'(?:https?://)?(?:www\.)?github\.com/[\w\-\.]+'
            ],
            'medium': [
                r'(?:https?://)?(?:www\.)?medium\.com/@?[\w\-\.]+'
            ],
            'pinterest': [
                r'(?:https?://)?(?:www\.)?pinterest\.com/[\w\-\.]+'
            ],
            'twitch': [
                r'(?:https?://)?(?:www\.)?twitch\.tv/[\w\-]+'
            ],
            'vk': [
                r'(?:https?://)?(?:www\.)?vk\.com/[\w\-\.]+'
            ],
            'whatsapp': [
                r'(?:https?://)?(?:www\.)?wa\.me/[\d]+',
                r'(?:https?://)?(?:www\.)?api\.whatsapp\.com/send\?phone=[\d]+'
            ],
            'wechat': [
                r'weixin://[\w\-]+',
                r'(?:https?://)?(?:www\.)?wechat\.com/[\w\-]+'
            ],
            'kakao': [
                r'(?:https?://)?(?:www\.)?pf\.kakao\.com/[\w\-]+',
                r'kakaotalk://[\w\-]+'
            ],
            'line': [
                r'(?:https?://)?(?:www\.)?line\.me/[\w\-]+',
                r'line://[\w\-]+'
            ]
        }
    
    def extract_all_sns_links(self, html_content, base_url):
        """
        Extract all social media links from HTML content
        """
        print("[SNS] Extracting social media links...")
        
        all_links = []
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all links in the page
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            
            # Check against all platform patterns
            for platform, patterns in self.platform_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, href, re.IGNORECASE):
                        link_data = {
                            'platform': platform,
                            'url': href,
                            'username': self.parse_username(href, platform),
                            'type': self.detect_link_type(href, platform),
                            'context': self.get_link_context(a_tag),
                            'validation': None,
                            'metadata': {}
                        }
                        all_links.append(link_data)
                        break
        
        # Remove duplicates
        unique_links = []
        seen_urls = set()
        for link in all_links:
            if link['url'] not in seen_urls:
                unique_links.append(link)
                seen_urls.add(link['url'])
        
        print(f"[SNS] Found {len(unique_links)} unique social media links across {len(set(l['platform'] for l in unique_links))} platforms")
        
        return unique_links
    
    def parse_username(self, url, platform):
        """
        Extract username/handle from social media URL
        """
        try:
            parsed = urlparse(url)
            path = parsed.path.strip('/')
            
            if platform == 'facebook':
                if 'profile.php' in url:
                    query = parse_qs(parsed.query)
                    return f"ID:{query.get('id', ['unknown'])[0]}"
                else:
                    parts = path.split('/')
                    return parts[-1] if parts else 'unknown'
            
            elif platform in ['twitter', 'instagram', 'tiktok', 'twitch', 'github', 'reddit']:
                parts = path.split('/')
                username = parts[-1] if parts else 'unknown'
                return username.lstrip('@')
            
            elif platform == 'linkedin':
                parts = path.split('/')
                return parts[-1] if len(parts) > 1 else 'unknown'
            
            elif platform in ['telegram', 'discord']:
                parts = path.split('/')
                return parts[-1] if parts else 'unknown'
            
            elif platform == 'youtube':
                if '@' in path:
                    return path.split('@')[-1]
                elif '/channel/' in path:
                    return path.split('/channel/')[-1]
                elif '/c/' in path:
                    return path.split('/c/')[-1]
                elif '/user/' in path:
                    return path.split('/user/')[-1]
                return 'unknown'
            
            elif platform == 'whatsapp':
                if 'phone=' in url:
                    query = parse_qs(parsed.query)
                    return query.get('phone', ['unknown'])[0]
                return path.split('/')[-1]
            
            else:
                parts = path.split('/')
                return parts[-1] if parts else 'unknown'
                
        except Exception as e:
            return 'unknown'
    
    def detect_link_type(self, url, platform):
        """
        Detect if link is profile, page, group, channel, etc.
        """
        url_lower = url.lower()
        
        if platform == 'facebook':
            if 'pages/' in url_lower:
                return 'page'
            elif 'groups/' in url_lower:
                return 'group'
            elif 'profile.php' in url_lower:
                return 'profile'
            return 'page/profile'
        
        elif platform == 'linkedin':
            if '/company/' in url_lower:
                return 'company'
            elif '/in/' in url_lower:
                return 'personal'
            return 'profile'
        
        elif platform == 'telegram':
            if 't.me/joinchat' in url_lower:
                return 'private_group'
            return 'channel/group'
        
        elif platform == 'discord':
            return 'server_invite'
        
        elif platform == 'reddit':
            if '/r/' in url_lower:
                return 'subreddit'
            elif '/u/' in url_lower or '/user/' in url_lower:
                return 'user'
            return 'community'
        
        elif platform == 'youtube':
            if '/channel/' in url_lower:
                return 'channel'
            elif '/c/' in url_lower or '/user/' in url_lower or '@' in url_lower:
                return 'channel'
            return 'channel'
        
        return 'profile'
    
    def get_link_context(self, a_tag):
        """
        Extract context information about where the link appears
        """
        context = {
            'location': 'unknown',
            'nearby_text': '',
            'section': ''
        }
        
        try:
            # Get link text
            link_text = a_tag.get_text(strip=True)
            
            # Find parent section
            parent = a_tag.find_parent(['header', 'footer', 'nav', 'aside', 'section', 'div'])
            if parent:
                if parent.name == 'header':
                    context['location'] = 'header'
                elif parent.name == 'footer':
                    context['location'] = 'footer'
                elif parent.name == 'nav':
                    context['location'] = 'navigation'
                else:
                    # Check class/id for hints
                    classes = ' '.join(parent.get('class', []))
                    id_attr = parent.get('id', '')
                    
                    if 'footer' in classes.lower() or 'footer' in id_attr.lower():
                        context['location'] = 'footer'
                    elif 'header' in classes.lower() or 'header' in id_attr.lower():
                        context['location'] = 'header'
                    elif 'social' in classes.lower() or 'social' in id_attr.lower():
                        context['location'] = 'social_section'
                    elif 'contact' in classes.lower() or 'contact' in id_attr.lower():
                        context['location'] = 'contact_section'
                    else:
                        context['location'] = 'content'
                
                context['section'] = parent.get('class', [''])[0] if parent.get('class') else parent.name
            
            # Get nearby text
            if a_tag.parent:
                nearby = a_tag.parent.get_text(strip=True)
                context['nearby_text'] = nearby[:100] if nearby else link_text
            else:
                context['nearby_text'] = link_text
                
        except Exception as e:
            pass
        
        return context
    
    def validate_link(self, url, timeout=5):
        """
        Validate if social media link is active
        """
        try:
            response = self.session.head(url, timeout=timeout, allow_redirects=True)
            return {
                'is_valid': response.status_code < 400,
                'status_code': response.status_code,
                'redirects_to': response.url if response.url != url else None
            }
        except Exception as e:
            return {
                'is_valid': False,
                'status_code': 0,
                'error': str(e)
            }
    
    def fetch_profile_metadata(self, link_data):
        """
        Fetch public profile metadata for a social media link
        Uses web scraping as fallback when APIs are not available
        """
        platform = link_data['platform']
        url = link_data['url']
        
        try:
            # Platform-specific metadata extraction
            if platform == 'twitter':
                return self._fetch_twitter_metadata(url)
            elif platform == 'instagram':
                return self._fetch_instagram_metadata(url)
            elif platform == 'facebook':
                return self._fetch_facebook_metadata(url)
            elif platform == 'youtube':
                return self._fetch_youtube_metadata(url)
            elif platform == 'linkedin':
                return self._fetch_linkedin_metadata(url)
            elif platform == 'tiktok':
                return self._fetch_tiktok_metadata(url)
            elif platform == 'github':
                return self._fetch_github_metadata(url)
            else:
                return self._fetch_generic_metadata(url)
                
        except Exception as e:
            print(f"[SNS] Failed to fetch metadata for {platform}: {e}")
            return {'error': str(e)}
    
    def _fetch_generic_metadata(self, url):
        """
        Generic metadata extraction from Open Graph tags
        """
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            metadata = {}
            
            # Open Graph tags
            og_tags = {
                'title': soup.find('meta', property='og:title'),
                'description': soup.find('meta', property='og:description'),
                'image': soup.find('meta', property='og:image'),
            }
            
            for key, tag in og_tags.items():
                if tag and tag.get('content'):
                    metadata[key] = tag['content']
            
            # Twitter Card tags
            if not metadata.get('title'):
                twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
                if twitter_title:
                    metadata['title'] = twitter_title.get('content', '')
            
            return metadata
            
        except Exception as e:
            return {'error': str(e)}
    
    def _fetch_twitter_metadata(self, url):
        """Extract Twitter profile metadata"""
        return self._fetch_generic_metadata(url)
    
    def _fetch_instagram_metadata(self, url):
        """Extract Instagram profile metadata"""
        return self._fetch_generic_metadata(url)
    
    def _fetch_facebook_metadata(self, url):
        """Extract Facebook page metadata"""
        return self._fetch_generic_metadata(url)
    
    def _fetch_youtube_metadata(self, url):
        """Extract YouTube channel metadata"""
        return self._fetch_generic_metadata(url)
    
    def _fetch_linkedin_metadata(self, url):
        """Extract LinkedIn profile/company metadata"""
        return self._fetch_generic_metadata(url)
    
    def _fetch_tiktok_metadata(self, url):
        """Extract TikTok profile metadata"""
        return self._fetch_generic_metadata(url)
    
    def _fetch_github_metadata(self, url):
        """Extract GitHub profile metadata using API"""
        try:
            username = url.rstrip('/').split('/')[-1]
            api_url = f"https://api.github.com/users/{username}"
            
            response = self.session.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'name': data.get('name', ''),
                    'bio': data.get('bio', ''),
                    'followers': data.get('followers', 0),
                    'public_repos': data.get('public_repos', 0),
                    'created_at': data.get('created_at', '')
                }
        except Exception as e:
            pass
        
        return self._fetch_generic_metadata(url)
    
    def extract_metadata_tags(self, html_content):
        """
        Extract social media metadata from HTML meta tags
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        metadata = {}
        
        # Open Graph tags
        og_tags = soup.find_all('meta', property=re.compile(r'^og:'))
        for tag in og_tags:
            prop = tag.get('property', '').replace('og:', '')
            content = tag.get('content', '')
            if prop and content:
                metadata[f'og_{prop}'] = content
        
        # Twitter Card tags
        twitter_tags = soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')})
        for tag in twitter_tags:
            name = tag.get('name', '').replace('twitter:', '')
            content = tag.get('content', '')
            if name and content:
                metadata[f'twitter_{name}'] = content
        
        # Facebook App ID
        fb_app_id = soup.find('meta', property='fb:app_id')
        if fb_app_id:
            metadata['facebook_app_id'] = fb_app_id.get('content', '')
        
        return metadata
    
    def calculate_presence_score(self, sns_data):
        """
        Calculate social media presence score (0-10)
        """
        score = 0
        
        # Platform diversity (0-4 points)
        num_platforms = len(set(link['platform'] for link in sns_data))
        score += min(num_platforms * 0.5, 4)
        
        # Link placement (0-2 points)
        header_footer_links = sum(1 for link in sns_data 
                                  if link['context']['location'] in ['header', 'footer'])
        if header_footer_links > 0:
            score += 2
        
        # Validation (0-2 points)
        valid_links = sum(1 for link in sns_data 
                         if link.get('validation', {}).get('is_valid', False))
        if valid_links > 0:
            score += min(valid_links * 0.5, 2)
        
        # Metadata availability (0-2 points)
        links_with_metadata = sum(1 for link in sns_data 
                                  if link.get('metadata') and len(link['metadata']) > 1)
        if links_with_metadata > 0:
            score += min(links_with_metadata * 0.4, 2)
        
        return round(min(score, 10), 1)
    
    def analyze_sns_presence(self, html_content, base_url, validate_links=True, fetch_metadata=True):
        """
        Complete SNS presence analysis
        """
        print("[SNS] Starting comprehensive social media analysis...")
        
        # Extract all links
        sns_links = self.extract_all_sns_links(html_content, base_url)
        
        # Extract metadata tags
        meta_tags = self.extract_metadata_tags(html_content)
        
        # Validate links if requested
        if validate_links and sns_links:
            print(f"[SNS] Validating {len(sns_links)} links...")
            for i, link in enumerate(sns_links):
                if i < 20:  # Limit to first 20 to avoid too many requests
                    link['validation'] = self.validate_link(link['url'])
                    time.sleep(0.5)  # Rate limiting
        
        # Fetch metadata if requested
        if fetch_metadata and sns_links:
            print(f"[SNS] Fetching metadata for profiles...")
            for i, link in enumerate(sns_links):
                if i < 10:  # Limit to first 10 to avoid too many requests
                    link['metadata'] = self.fetch_profile_metadata(link)
                    time.sleep(1)  # Rate limiting
        
        # Calculate presence score
        presence_score = self.calculate_presence_score(sns_links)
        
        result = {
            'links': sns_links,
            'meta_tags': meta_tags,
            'presence_score': presence_score,
            'summary': {
                'total_links': len(sns_links),
                'platforms': list(set(link['platform'] for link in sns_links)),
                'platform_count': len(set(link['platform'] for link in sns_links))
            }
        }
        
        print(f"[SNS] Analysis complete. Found {len(sns_links)} links across {result['summary']['platform_count']} platforms")
        print(f"[SNS] Social Presence Score: {presence_score}/10")
        
        return result
