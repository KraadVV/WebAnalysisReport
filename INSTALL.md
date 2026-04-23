# Installation Guide - Web Analysis Report Tool

## Quick Start

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- playwright (browser automation)
- beautifulsoup4 (HTML parsing)
- python-docx (report generation)
- ipwhois (IP analysis)
- requests (HTTP requests)
- python-whois (domain WHOIS)
- dnspython (DNS queries)

### 2. Install Playwright Browsers

```bash
playwright install chromium
```

This downloads the Chromium browser (~170MB) that Playwright will use.

### 3. Run the Tool

```bash
python test.py
```

## Configuration

### Basic Settings (config.py)

```python
TARGET_URL = "https://www.google.com"  # Default URL
HEADLESS_MODE = True                    # False to see browser
VIEWPORT_SIZE = {"width": 1280, "height": 720}
```

### SNS Analysis Settings

```python
SNS_VALIDATE_LINKS = True   # Check if links are active
SNS_FETCH_METADATA = True   # Fetch profile information
SNS_MAX_VALIDATE = 20       # Max links to validate
SNS_MAX_METADATA = 10       # Max profiles to fetch
```

### Optional: API Keys for Enhanced SNS Analysis

Edit `config.py` and add your API keys:

```python
SNS_API_KEYS = {
    'twitter_bearer_token': 'YOUR_TOKEN_HERE',
    'youtube_api_key': 'YOUR_KEY_HERE',
    # ... other keys
}
```

**How to get API keys:**

- **Twitter**: https://developer.twitter.com/en/portal/dashboard
- **YouTube**: https://console.cloud.google.com/apis/credentials
- **Reddit**: https://www.reddit.com/prefs/apps
- **Telegram**: Create a bot via @BotFather

**Note**: API keys are optional. The tool works without them using web scraping.

## Troubleshooting

### Issue: "Playwright not found"
**Solution**: Run `playwright install chromium`

### Issue: "Chrome.exe not found" (when running as EXE)
**Solution**: 
- Place `chrome-win64` folder next to the EXE
- Or let it use Playwright's bundled Chromium (automatic fallback)

### Issue: "WHOIS lookup failed"
**Solution**: Some domains block WHOIS queries. This is normal.

### Issue: "SNS metadata fetch failed"
**Solution**: 
- Some platforms block automated access
- Rate limiting may be in effect
- Try adding API keys for better results

### Issue: "SSL certificate error"
**Solution**: The target site may not use HTTPS or has certificate issues.

## Performance Tips

1. **Disable SNS metadata fetching** for faster analysis:
   ```python
   SNS_FETCH_METADATA = False
   ```

2. **Reduce validation limits** to speed up:
   ```python
   SNS_MAX_VALIDATE = 5
   SNS_MAX_METADATA = 3
   ```

3. **Use headless mode** for better performance:
   ```python
   HEADLESS_MODE = True
   ```

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 500MB for dependencies and browsers
- **Internet**: Required for analysis and OSINT lookups
- **OS**: Windows, macOS, or Linux

## First Run Example

```bash
# Install everything
pip install -r requirements.txt
playwright install chromium

# Run with default settings
python test.py

# When prompted:
# 1. Press Enter to use default URL (google.com)
# 2. Type 'n' for no login required
# 3. Wait for analysis to complete
# 4. Check outputs/ folder for the report
```

## Advanced Usage

### Analyze a specific website
```bash
python test.py
# Enter: https://megapari.games
```

### Analyze with login
```bash
python test.py
# Enter target URL
# Type 'y' when asked about login
# Enter login page URL
# Complete login in browser window
# Press Enter to continue analysis
```

## Output

Reports are saved to:
```
outputs/
├── report_YYYYMMDD_HHMMSS.docx
└── screenshots/
    ├── capture_YYYYMMDD_HHMMSS.png
    └── elements/
        ├── elem_0_xxx.png
        ├── elem_1_xxx.png
        └── ...
```

## Support

For issues or questions:
1. Check this installation guide
2. Review CHANGELOG.md for recent changes
3. Check GitHub issues
4. Create a new issue with error details
