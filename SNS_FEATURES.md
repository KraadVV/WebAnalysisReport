# Advanced SNS Analysis Features

## Overview

The Web Analysis Report Tool now includes comprehensive social media intelligence gathering capabilities. This document details the SNS analysis features.

## Supported Platforms (18+)

### Major Platforms
1. **Facebook** - Pages, Profiles, Groups
2. **Twitter/X** - Personal and Business accounts
3. **Instagram** - Profiles and Business accounts
4. **LinkedIn** - Personal profiles and Company pages
5. **YouTube** - Channels and User accounts
6. **TikTok** - Creator profiles

### Messaging & Community
7. **Telegram** - Channels, Groups, Bots
8. **Discord** - Server invites
9. **WhatsApp** - Business links
10. **WeChat** - Official accounts
11. **KakaoTalk** - Business profiles
12. **Line** - Official accounts

### Content & Development
13. **GitHub** - User and Organization profiles
14. **Medium** - Writer profiles
15. **Reddit** - Users and Subreddits
16. **Pinterest** - Boards and profiles

### Streaming & Other
17. **Twitch** - Streamer channels
18. **VK** - Russian social network profiles

## Features

### 1. Link Extraction
- **Comprehensive Pattern Matching**: Uses advanced regex to find all social media links
- **Multiple URL Formats**: Handles various URL patterns (www, mobile, short links)
- **Deduplication**: Automatically removes duplicate links
- **Context Awareness**: Identifies where links appear on the page

### 2. Username Parsing
Automatically extracts usernames/handles from URLs:
- `https://twitter.com/megapari` → `megapari`
- `https://instagram.com/megapari_official` → `megapari_official`
- `https://t.me/megapari_en` → `megapari_en`
- `https://facebook.com/profile.php?id=123456` → `ID:123456`

### 3. Link Type Detection
Identifies the type of social media link:
- **Profile** - Personal account
- **Page** - Business/Brand page
- **Group** - Community group
- **Channel** - Broadcast channel
- **Company** - Corporate profile
- **Subreddit** - Reddit community

### 4. Context Detection
Determines where links appear:
- **Header** - Top navigation
- **Footer** - Bottom of page
- **Social Section** - Dedicated social media area
- **Contact Section** - Contact information area
- **Content** - Within page content
- **Navigation** - Menu items

### 5. Link Validation
Checks if links are active:
- HTTP HEAD request to verify status
- Status code tracking (200, 404, etc.)
- Redirect detection
- Error handling for unreachable links

### 6. Profile Metadata Extraction
Fetches public information from profiles:

#### Generic (All Platforms)
- Open Graph title, description, image
- Twitter Card metadata
- Page title and meta tags

#### GitHub (API-based)
- Name and bio
- Follower count
- Public repository count
- Account creation date

#### Other Platforms (Web Scraping)
- Profile titles
- Descriptions
- Public metadata tags

### 7. Metadata Tag Parsing
Extracts social media metadata from HTML:
- **Open Graph tags**: `og:title`, `og:description`, `og:image`, `og:url`, etc.
- **Twitter Card tags**: `twitter:card`, `twitter:site`, `twitter:creator`, etc.
- **Facebook App ID**: For Facebook integration detection

### 8. Presence Scoring
Calculates a social media presence score (0-10) based on:
- **Platform Diversity** (0-4 points): More platforms = higher score
- **Link Placement** (0-2 points): Header/footer placement indicates official presence
- **Link Validation** (0-2 points): Active links score higher
- **Metadata Availability** (0-2 points): Rich metadata indicates active management

**Score Interpretation:**
- **8-10**: Excellent - Strong social media presence
- **6-7.9**: Good - Solid social media utilization
- **4-5.9**: Average - Basic social media presence
- **0-3.9**: Poor - Limited social media presence

## Configuration

### Basic Settings (config.py)

```python
# Enable/disable link validation
SNS_VALIDATE_LINKS = True

# Enable/disable metadata fetching
SNS_FETCH_METADATA = True

# Maximum links to validate (to avoid rate limiting)
SNS_MAX_VALIDATE = 20

# Maximum profiles to fetch metadata for
SNS_MAX_METADATA = 10
```

### API Keys (Optional)

```python
SNS_API_KEYS = {
    'twitter_bearer_token': '',      # Twitter API v2
    'facebook_app_id': '',           # Facebook Graph API
    'facebook_app_secret': '',
    'youtube_api_key': '',           # YouTube Data API
    'reddit_client_id': '',          # Reddit API
    'reddit_client_secret': '',
    'telegram_bot_token': ''         # Telegram Bot API
}
```

**Note**: API keys are optional. The tool works without them using web scraping.

## Report Output

### Section 10: Deep SNS Analysis

The generated report includes:

#### 10-1. Discovered Social Media Accounts
Table with:
- Platform name
- Username/handle
- Link type (profile, page, channel, etc.)
- Location on page (header, footer, etc.)
- Validation status (✓ Active / ✗ Inactive)
- Full URL

#### 10-2. Social Media Metadata
Table showing:
- Open Graph tags
- Twitter Card tags
- Facebook App ID
- Other social metadata

#### 10-3. Profile Details
For each validated profile:
- Platform and username
- Profile title/name
- Bio/description
- Follower counts (if available)
- Additional metadata

#### 10-4. Analysis Summary
- Overall assessment (Excellent/Good/Average/Poor)
- Active platforms list
- Link placement statistics
- Validation statistics
- Social presence score

## Usage Examples

### Example 1: Basic Analysis
```python
from src.sns_analyzer import SNSAnalyzer

analyzer = SNSAnalyzer()
results = analyzer.analyze_sns_presence(
    html_content=html,
    base_url="https://example.com",
    validate_links=True,
    fetch_metadata=True
)

print(f"Found {results['summary']['total_links']} links")
print(f"Presence Score: {results['presence_score']}/10")
```

### Example 2: Extract Just Links
```python
analyzer = SNSAnalyzer()
links = analyzer.extract_all_sns_links(html, base_url)

for link in links:
    print(f"{link['platform']}: @{link['username']}")
```

### Example 3: Validate Specific Link
```python
analyzer = SNSAnalyzer()
validation = analyzer.validate_link("https://twitter.com/example")

if validation['is_valid']:
    print(f"Link is active (Status: {validation['status_code']})")
```

## Performance Considerations

### Rate Limiting
- Built-in delays between requests (0.5-1 second)
- Configurable limits on validation and metadata fetching
- Respects platform rate limits

### Timeout Protection
- 5-second timeout for link validation
- 10-second timeout for metadata fetching
- Graceful error handling

### Resource Usage
- Validation: ~0.5 seconds per link
- Metadata: ~1-2 seconds per profile
- Total time: Depends on number of links found

**Example**: 10 SNS links with validation and metadata:
- Validation: ~5 seconds
- Metadata: ~10-20 seconds
- Total: ~15-25 seconds additional analysis time

## Best Practices

### 1. For Quick Analysis
```python
SNS_VALIDATE_LINKS = False
SNS_FETCH_METADATA = False
```
This will only extract and parse links (very fast).

### 2. For Comprehensive Analysis
```python
SNS_VALIDATE_LINKS = True
SNS_FETCH_METADATA = True
SNS_MAX_VALIDATE = 20
SNS_MAX_METADATA = 10
```
This provides full analysis with validation and metadata.

### 3. For Production/Automated Scans
```python
SNS_VALIDATE_LINKS = True
SNS_FETCH_METADATA = False
SNS_MAX_VALIDATE = 10
```
Validates links but skips slow metadata fetching.

## Limitations

### Without API Keys
- Limited to publicly visible information
- Web scraping may be blocked by some platforms
- Rate limiting may affect results
- Some metadata may not be available

### With API Keys
- Better data quality and reliability
- Higher rate limits
- Access to more detailed information
- Requires setup and maintenance

### Platform-Specific
- **Instagram**: Heavily restricts automated access
- **Facebook**: Limited public data without app approval
- **LinkedIn**: Blocks most scraping attempts
- **Twitter/X**: Requires API key for reliable access
- **GitHub**: Public API works well without authentication

## Privacy & Ethics

### What We Collect
- Only publicly visible information
- Links that appear on the target website
- Public profile metadata (if available)

### What We Don't Do
- No authentication bypass attempts
- No private data access
- No violation of platform ToS
- No aggressive scraping

### Recommendations
- Use responsibly and ethically
- Respect platform rate limits
- Only analyze websites you have permission to analyze
- Follow all applicable laws and regulations

## Troubleshooting

### "No SNS links found"
- Website may not have social media links
- Links may use non-standard formats
- Check if JavaScript is required to load links

### "Validation failed for all links"
- Network connectivity issues
- Platform blocking automated requests
- Try reducing SNS_MAX_VALIDATE

### "Metadata fetch failed"
- Platform blocking automated access (common)
- Rate limiting in effect
- Try adding API keys for better results
- Reduce SNS_MAX_METADATA

### "Presence score is 0"
- No links found or validated
- All links failed validation
- Check website has social media presence

## Future Enhancements

Potential additions:
- API integration for major platforms (with user-provided keys)
- Follower count tracking over time
- Engagement metrics analysis
- Cross-platform username consistency checking
- Social media audit recommendations
- Automated profile screenshot capture
- Historical data comparison

## Support

For SNS analysis issues:
1. Check this documentation
2. Verify network connectivity
3. Try disabling metadata fetching
4. Check platform-specific limitations
5. Report issues on GitHub
