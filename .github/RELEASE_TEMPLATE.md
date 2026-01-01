## Threads Downloader v${VERSION}

### 📦 Downloads

| Platform | Interactive Mode (Double-click) | CLI Mode |
|----------|--------------------------------|----------|
| Windows | `threads-downloader-${VERSION}-windows-x64.exe` | `threads-downloader-cli-${VERSION}-windows-x64.exe` |
| macOS | `threads-downloader-${VERSION}-macos-x64` | `threads-downloader-cli-${VERSION}-macos-x64` |
| Linux | `threads-downloader-${VERSION}-linux-x64` | `threads-downloader-cli-${VERSION}-linux-x64` |

- **threads-downloader**: Interactive mode - double-click to run, follow prompts
- **threads-downloader-cli**: Command line mode - use with arguments

---

### 🚀 Quick Start

#### Interactive Mode (Double-click)

Simply double-click `threads-downloader-${VERSION}-{platform}` to launch:

```
==============================
Threads Downloader
==============================
Enter a Threads profile URL (blank to finish): https://www.threads.net/@username
Enter a Threads profile URL (blank to finish): 
Download folder [./downloads]: 
Run Chrome headless? (Y/n): 
Concurrent downloads [3]: 
Cookie file path [cookies.pkl]: 
```

#### CLI Mode

##### Windows
```cmd
.\threads-downloader-cli-${VERSION}-windows-x64.exe --profile https://www.threads.net/@username
```

##### macOS / Linux
```bash
chmod +x threads-downloader-cli-${VERSION}-linux-x64
./threads-downloader-cli-${VERSION}-linux-x64 --profile https://www.threads.net/@username
```

---

### 📋 CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--profile URL [URL ...]` | One or more profile URLs to download (required) | - |
| `--out DIR` | Download directory | `./downloads` |
| `--headless` | Run Chrome in headless mode | `True` |
| `--workers N` | Number of concurrent download threads | `3` |
| `--cookies_path FILE` | Path to cookies file | `cookies.pkl` |

---

### 💡 CLI Examples

```bash
# Download from a single profile
threads-downloader-cli --profile https://www.threads.net/@username

# Download from multiple profiles
threads-downloader-cli --profile https://www.threads.net/@user1 https://www.threads.net/@user2

# Custom output directory with 8 download workers
threads-downloader-cli --profile https://www.threads.net/@username --out ./my_downloads --workers 8
```

---

### 🔐 First Run - Authentication

On first run, the tool will:
1. Open a browser window automatically
2. Navigate to Threads login page
3. Wait for you to log in manually
4. Press Enter in the terminal after logging in
5. Save cookies for future sessions

---

### ⚠️ Notes

- **Chrome Required**: Make sure Google Chrome is installed on your system.
- **Cookies**: Login session is saved to `cookies.pkl` and reused automatically.
- **Output**: Files are saved to `./downloads/{username}/` by default.
