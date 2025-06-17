# Threads Downloader

A powerful Python tool for downloading images and videos from Instagram Threads profiles. Supports batch processing of multiple profiles with concurrent downloads.

## ✨ Features

- **Multi-profile support** - Download from multiple Threads profiles in one command
- **Automatic authentication** - Cookie-based login system with persistent sessions
- **Concurrent downloads** - Configurable worker threads for faster processing
- **Stealth mode** - Anti-detection browser automation to avoid blocks
- **Flexible output** - Organized downloads by author with customizable directories

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/911218sky/threads-downloader.git
cd threads-downloader
pip install -e .
```

### Basic Usage
```bash
# Download from a single profile
threads-downloader --profile https://www.threads.com/@username

# Download from multiple profiles
threads-downloader --profile https://www.threads.com/@user1 https://www.threads.com/@user2

# Custom output directory with more workers
threads-downloader --profile https://www.threads.com/@username --out ./my_downloads --workers 8
```

## 📋 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--profile` | One or more profile URLs to scrape (required) | - |
| `--out` | Download directory | `./downloads` |
| `--headless` | Run Chrome in headless mode | `True` |
| `--workers` | Number of concurrent download threads | `3` |
| `--cookies_path` | Path to cookies file | `cookies.pkl` |

## 🔐 Authentication

On first run, the tool will automatically open a browser window for you to log in to Threads. Your session will be saved as cookies for future use.

```bash
# The tool will prompt you when authentication is needed
Please log in to Threads in the newly opened browser window. 
After you have finished logging in, return to this terminal and press Enter to automatically save your cookies.
```

## 🛠 Advanced Usage

### Headless Mode (Default)
```bash
threads-downloader --profile https://www.threads.com/@username --headless
```

### Visible Browser (for debugging)
```bash
threads-downloader --profile https://www.threads.com/@username --no-headless
```

### High-Performance Download
```bash
threads-downloader --profile https://www.threads.com/@username --workers 16
```

### Custom Cookie Location
```bash
threads-downloader --profile https://www.threads.com/@username --cookies_path ./custom_cookies.pkl
```

## ⚠️ Important Notes

- **Rate Limiting**: The tool includes built-in delays to avoid overwhelming Threads servers
- **Authentication**: Cookies are automatically saved and reused across sessions
- **File Naming**: Files are prefixed with post order and use UUID7 for uniqueness
- **Error Handling**: Failed downloads are logged but don't stop the overall process