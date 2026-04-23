# Changelog - Web Analysis Report Tool

## Version 2.1 - Advanced SNS Intelligence (2026-04-23)

### 🎉 Major New Features

#### **Comprehensive Social Media Analysis**
- **NEW MODULE**: `sns_analyzer.py` - Dedicated SNS intelligence gathering
- **18+ Platform Support**: Facebook, Twitter/X, Instagram, LinkedIn, YouTube, TikTok, Telegram, Discord, Reddit, GitHub, Medium, Pinterest, Twitch, VK, WhatsApp, WeChat, KakaoTalk, Line
- **Username Extraction**: Automatically parses usernames/handles from all URL formats
- **Link Validation**: HTTP status checking for all discovered links
- **Profile Metadata**: Fetches public profile information (Open Graph, Twitter Cards, API data)
- **Context Detection**: Identifies where links appear (header, footer, social section, etc.)
- **Presence Scoring**: Calculates 0-10 score based on platform diversity, placement, and validation
- **Enhanced Reporting**: New Section 10 with detailed SNS analysis tables

### 📦 New Configuration Options

Added to `config.py`:
```python
SNS_VALIDATE_LINKS = True
SNS_FETCH_METADATA = True
SNS_MAX_VALIDATE = 20
SNS_MAX_METADATA = 10
SNS_API_KEYS = {...}
```

### 📊 Enhanced Report Structure

**New Section 10: Deep SNS Analysis**
- 10-1. Discovered Social Media Accounts (table)
- 10-2. Social Media Metadata (Open Graph, Twitter Cards)
- 10-3. Profile Details (with fetched metadata)
- 10-4. Analysis Summary (presence score, statistics)

### 📝 New Documentation

- `SNS_FEATURES.md` - Comprehensive SNS feature documentation
- `INSTALL.md` - Detailed installation and configuration guide
- Updated `README.md` with new features

### 🚀 Performance

- Configurable rate limiting for SNS requests
- Parallel-ready architecture
- Graceful degradation when platforms block access
- Smart caching to avoid duplicate requests

---

## Version 2.0 - Enhanced OSINT & Network Analysis (2026-04-23)

### 🎉 Major New Features

#### 1. **Comprehensive Network Resource Tracking**
- **ALL network resources** are now captured (not just XHR/Fetch)
- Tracks: images, stylesheets, scripts, fonts, media, websockets, and more
- Resource type statistics and categorization
- Complete IP mapping for all external connections

#### 2. **OSINT (Open Source Intelligence) Analysis**
- **Domain WHOIS Information**
  - Registrar details
  - Creation and expiration dates
  - Organization information
  - Name servers
  - Contact emails (if public)

- **DNS Records Analysis**
  - A records (IP addresses)
  - MX records (mail servers)
  - TXT records (SPF, DKIM, etc.)
  - NS records (name servers)

- **SSL/TLS Certificate Analysis**
  - Certificate issuer
  - Validity period
  - Subject information
  - Subject Alternative Names (SANs)

- **Technology Stack Detection**
  - Frontend frameworks (React, Vue, Angular, jQuery, etc.)
  - CMS platforms (WordPress, Drupal, Joomla, Shopify, Wix)
  - Analytics tools (Google Analytics, GTM, Facebook Pixel, etc.)
  - Web server identification
  - Programming language detection

- **Contact Information Extraction**
  - Email addresses found on page
  - Phone numbers (Korean and international formats)
  - Social media links (Facebook, Twitter, LinkedIn, Instagram, YouTube, GitHub)

### 🔧 Bug Fixes

1. **Fixed Chrome.exe Path Issue**
   - Eliminated code duplication in `browser_handler.py`
   - Proper fallback to Playwright's bundled Chromium
   - Better error handling and user feedback

2. **Fixed test.py Bugs**
   - Line 34: Removed unnecessary parentheses in `login_url` initialization
   - Line 75: Removed redundant `network_tracker.start_tracing()` call
   - Line 103: Removed premature `save_file()` call before report creation

### 📦 Dependencies Added

- `python-whois>=0.8.0` - Domain WHOIS lookups
- `dnspython>=2.4.0` - DNS record queries
- Updated `requirements.txt` with all dependencies

### 📊 Enhanced Report Sections

The generated DOCX report now includes:

1. Initial Screen Capture
2. Page Structure Analysis
3. API Communication Analysis
4. Server IP WHOIS Information
5. Interactive Elements Analysis
6. **NEW: Complete Network Resource Analysis**
   - Resource type statistics
   - All unique IP addresses contacted
7. **NEW: OSINT Information Analysis**
   - Domain WHOIS data
   - DNS records
   - SSL/TLS certificate details
8. **NEW: Technology Stack Analysis**
   - Detected frameworks and libraries
   - CMS identification
   - Analytics tools
9. **NEW: Contact & Social Media Information**
   - Extracted emails and phone numbers
   - Social media presence

### 🚀 Performance Improvements

- Optimized network tracking to handle all resource types efficiently
- Better error handling for OSINT lookups
- Graceful degradation when services are unavailable

### 📝 Code Quality

- Refactored browser launch logic (eliminated duplication)
- Added comprehensive docstrings
- Improved error messages
- Better separation of concerns with new `osint_analyzer.py` module

---

## Version 1.0 - Initial Release

### Features
- Automated browser interaction with Playwright
- Network traffic analysis
- HTML structure parsing
- Interactive element detection
- WHOIS IP analysis
- DOCX report generation
- Login support for authenticated pages
- Lazy loading handling
