# Threads Downloader

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/github/license/911218sky/threads-downloader" alt="License">
  <img src="https://img.shields.io/github/v/release/911218sky/threads-downloader" alt="Release">
</p>

A powerful Python tool for downloading images and videos from Instagram Threads profiles. Supports batch processing of multiple profiles with concurrent downloads.

## ✨ Features

- 🔄 **Multi-profile Support** - Download from multiple Threads profiles in one command
- 🔐 **Auto Authentication** - Cookie-based login system with persistent sessions
- ⚡ **Concurrent Downloads** - Configurable worker threads for faster processing
- 🛡️ **Stealth Mode** - Anti-detection browser automation to avoid blocks
- 📁 **Flexible Output** - Organized downloads by author with customizable directories

## 📦 Installation

### Option 1: Download Pre-built Binaries (Recommended)

Go to the [Releases](https://github.com/911218sky/threads-downloader/releases) page and download the executable for your system:

| Platform | File |
|----------|------|
| Windows | `threads-downloader-{version}-windows-x64.exe` |
| macOS | `threads-downloader-{version}-macos-x64` |
| Linux | `threads-downloader-{version}-linux-x64` |

Extract and run directly.

### Option 2: Install from Source

```bash
git clone https://github.com/911218sky/threads-downloader.git
cd threads-downloader

# Automatic setup (recommended)
# Windows
scripts\setup.bat

# macOS / Linux
chmod +x scripts/setup.sh
./scripts/setup.sh
```

The setup script will:
- Check if Conda is installed (offer to install Miniconda if not)
- Create a Python 3.12 virtual environment
- Install all dependencies
- Install the package in editable mode

#### Manual Installation

```bash
conda create -p venv python=3.12
conda activate ./venv
pip install -r requirements.txt
pip install -e .
```

## 🚀 Quick Start

### CLI Mode

```bash
# Download from a single profile
threads-downloader --profile https://www.threads.net/@username

# Download from multiple profiles
threads-downloader --profile https://www.threads.net/@user1 https://www.threads.net/@user2

# Custom output directory with more workers
threads-downloader --profile https://www.threads.net/@username --out ./my_downloads --workers 8
```

### Interactive Mode

```bash
# Windows
start.bat

# macOS / Linux
./start.sh

# Or run directly
python src/main.py
```

## 📋 CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--profile` | One or more profile URLs to scrape (required) | - |
| `--out` | Download directory | `./downloads` |
| `--headless` | Run Chrome in headless mode | `True` |
| `--no-headless` | Show browser window (for debugging) | - |
| `--workers` | Number of concurrent download threads | `3` |
| `--cookies_path` | Path to cookies file | `cookies.pkl` |

## 🔐 Authentication

On first run, the tool will automatically open a browser window for you to log in to Threads. Your session will be saved as cookies for future use.

```
Please log in to Threads in the newly opened browser window.
After you have finished logging in, return to this terminal and press Enter to automatically save your cookies.
```

## 🛠️ Advanced Usage

```bash
# High-performance download (16 workers)
threads-downloader --profile https://www.threads.net/@username --workers 16

# Visible browser (for debugging)
threads-downloader --profile https://www.threads.net/@username --no-headless

# Custom cookie location
threads-downloader --profile https://www.threads.net/@username --cookies_path ./my_cookies.pkl
```

## 📁 Project Structure

```
threads-downloader/
├── src/
│   └── threads_downloader/    # Main package
│       ├── cli.py             # Command-line interface
│       ├── config.py          # Configuration
│       ├── downloader.py      # Download logic
│       ├── driver.py          # Browser automation
│       ├── scraper.py         # Media scraping
│       └── utils.py           # Utilities
├── scripts/
│   ├── setup.bat              # Windows setup script
│   ├── setup.sh               # macOS/Linux setup script
│   ├── release.bat            # Windows release script
│   └── release.sh             # macOS/Linux release script
├── .github/
│   ├── workflows/
│   │   └── build-release.yml  # CI/CD workflow
│   └── RELEASE_TEMPLATE.md    # Release notes template
├── start.bat                  # Windows quick start
├── start.sh                   # macOS/Linux quick start
└── requirements.txt           # Dependencies
```

## ⚠️ Important Notes

- **Rate Limiting**: Built-in delays to avoid overwhelming Threads servers
- **Authentication**: Cookies are automatically saved and reused across sessions
- **File Naming**: Files are prefixed with post order and use UUID7 for uniqueness
- **Error Handling**: Failed downloads are logged but don't stop the overall process

## 🔧 Development

### Release a New Version

```bash
# Windows
scripts\release.bat

# macOS / Linux
./scripts/release.sh
```

The release script will:
1. Show current version
2. Let you choose version bump type (patch/minor/major)
3. Update `pyproject.toml`
4. Create git tag and push to GitHub
5. Trigger GitHub Actions to build binaries

## 📄 License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Issues and Pull Requests are welcome!
