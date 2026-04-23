# Chrome Auto-Detection Feature

## Overview

The WebAnalysisReport tool now includes an intelligent Chrome browser detection system that automatically finds and uses Chrome on your system, with fallback options if Chrome is not found.

## How It Works

### Detection Flow

```
1. Load Saved Preferences (user_config.json)
   ├─ If user previously chose Playwright Chromium → Use it
   ├─ If user previously provided custom path → Validate and use it
   └─ If no saved preference → Continue to auto-detection

2. Auto-Detection (Silent, Automatic)
   ├─ Check Windows Registry (most reliable)
   ├─ Check common installation paths:
   │  ├─ C:\Program Files\Google\Chrome\Application\chrome.exe
   │  ├─ C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
   │  └─ %LOCALAPPDATA%\Google\Chrome\Application\chrome.exe
   ├─ Check bundled chrome-win64/chrome.exe (for EXE distribution)
   └─ If found → Use it ✓

3. Interactive User Prompt (if auto-detection fails)
   ├─ Display searched locations
   ├─ Offer 2 options:
   │  [1] Use Playwright's Chromium (safe fallback)
   │  [2] Provide custom Chrome path
   └─ Save user's choice to user_config.json
```

## User Experience

### Scenario 1: Chrome Found Automatically (Most Common)
```
[Browser] Launching browser...
[Browser] Auto-detecting Chrome installation...
[Browser] ✓ Found Chrome via Windows Registry: C:\Program Files\Google\Chrome\Application\chrome.exe
[Browser] Launching Chrome: C:\Program Files\Google\Chrome\Application\chrome.exe
[Browser] Browser launched successfully.
```

**No user interaction required!** ✓

### Scenario 2: Chrome Not Found - User Prompted
```
[Browser] Launching browser...
[Browser] Auto-detecting Chrome installation...
[Browser] ✗ Not found: C:\Program Files\Google\Chrome\Application\chrome.exe
[Browser] ✗ Not found: C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
[Browser] ⚠️ Chrome not found in any standard location

======================================================================
⚠️  Chrome Browser Not Found!
======================================================================

Please choose an option:
  [1] Use Playwright's Chromium (recommended, works offline)
  [2] Provide custom Chrome path

Your choice (1 or 2): _
```

#### Option 1: Use Playwright's Chromium
```
Your choice (1 or 2): 1
[Browser] Using Playwright's bundled Chromium
[Browser] Saved preference to d:\ViveCode\WebAnalysisReport\WebAnalysisReport\user_config.json
[Browser] Launching Playwright's bundled Chromium
[Browser] Browser launched successfully.
```

#### Option 2: Provide Custom Path
```
Your choice (1 or 2): 2

Please enter the full path to chrome.exe
Example: C:\Program Files\Google\Chrome\Application\chrome.exe

Chrome path: D:\CustomApps\Chrome\chrome.exe
[Browser] ✓ Valid Chrome path: D:\CustomApps\Chrome\chrome.exe
[Browser] Saved preference to d:\ViveCode\WebAnalysisReport\WebAnalysisReport\user_config.json
[Browser] Launching Chrome: D:\CustomApps\Chrome\chrome.exe
[Browser] Browser launched successfully.
```

### Scenario 3: Using Saved Preference (Subsequent Runs)
```
[Browser] Launching browser...
[Browser] Using saved Chrome path: D:\CustomApps\Chrome\chrome.exe
[Browser] Launching Chrome: D:\CustomApps\Chrome\chrome.exe
[Browser] Browser launched successfully.
```

**User's choice is remembered!** ✓

## Configuration File

The tool saves your preference in `user_config.json` (automatically created):

```json
{
  "chrome_path": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "use_playwright_chromium": false
}
```

or

```json
{
  "chrome_path": null,
  "use_playwright_chromium": true
}
```

### Changing Your Preference

To change your browser preference:

1. **Delete** `user_config.json` from the project root
2. **Run the tool again** - you'll be prompted to choose again

Or manually edit `user_config.json` to change the path.

## Technical Details

### Auto-Detection Methods

1. **Windows Registry Lookup** (Most Reliable)
   - Checks: `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe`
   - Also checks: `HKEY_CURRENT_USER` registry

2. **Common Installation Paths**
   - Program Files (64-bit)
   - Program Files (x86) (32-bit)
   - Local AppData (user-specific installation)

3. **Bundled Chrome** (for EXE distribution)
   - Checks for `chrome-win64/chrome.exe` next to the executable

### Path Validation

When you provide a custom path, the tool validates:
- ✓ File exists
- ✓ Is a file (not a directory)
- ✓ Has `.exe` extension
- ✓ Is accessible

### Error Handling

If a saved path becomes invalid (e.g., Chrome uninstalled):
```
[Browser] ⚠️ Saved Chrome path no longer valid: C:\OldPath\chrome.exe
[Browser] Will attempt auto-detection...
```

The tool automatically tries to find Chrome again or prompts you for a new path.

## Benefits

✅ **Zero friction** - Auto-detects Chrome for most users  
✅ **User-friendly** - Clear prompts when needed  
✅ **Persistent** - Remembers your choice  
✅ **Flexible** - Supports custom Chrome locations  
✅ **Safe fallback** - Playwright Chromium always available  
✅ **Portable** - Works with USB/portable Chrome installations  
✅ **Smart validation** - Prevents invalid paths  

## Troubleshooting

### "Chrome not found" even though Chrome is installed

**Solution**: The tool will prompt you to provide the path manually. Find your chrome.exe location:
1. Open Chrome
2. Type `chrome://version` in the address bar
3. Look for "Executable Path"
4. Copy that path and provide it when prompted

### Want to switch from Chromium to Chrome (or vice versa)

**Solution**: Delete `user_config.json` and run the tool again to choose a different option.

### Custom Chrome installation not detected

**Solution**: Use Option 2 when prompted and provide the full path to your chrome.exe file.

## For Developers

### Key Functions

- `_load_user_config()` - Load saved preferences
- `_save_user_config()` - Save user's choice
- `_check_registry_chrome()` - Windows Registry lookup
- `_find_chrome_auto()` - Auto-detection logic
- `_validate_chrome_path()` - Path validation
- `_prompt_user_for_chrome()` - Interactive prompt

### Adding New Detection Methods

To add support for other browsers or paths, modify `_find_chrome_auto()`:

```python
# Add to search_paths list
search_paths.append(("Edge Browser", edge_path))
```

### Cross-Platform Support

Currently optimized for Windows. To add macOS/Linux support:

1. Modify `_find_chrome_auto()` to check platform
2. Add platform-specific paths
3. Replace `winreg` with platform-appropriate registry/config lookup

## Version History

- **v2.0** (2026-04-23): Initial release of Chrome auto-detection feature
  - Windows Registry support
  - Common path detection
  - Interactive user prompts
  - Config persistence via user_config.json
