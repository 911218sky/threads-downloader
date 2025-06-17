from pathlib import Path
import os
from typing import List

from threads_downloader.config import DL_WORKERS, DOWNLOAD_FOLDER, IS_HEADLESS
from threads_downloader.driver import build_stealth_driver
from threads_downloader.utils import load_cookies, save_cookies
from threads_downloader.scraper import collect_all_media, get_author_name
from threads_downloader.downloader import batch_download

def ensure_cookies(path: str) -> None:
    """Create a cookies file when it does not yet exist.

    The function opens a non-headless browser, waits for the user to log in,
    and then saves the retrieved cookies to *path*.
    """
    if not os.path.exists(path):
        print("First run detected – opening a browser for login …")
        driver = build_stealth_driver(headless=False)
        driver.get("https://www.threads.net/")
        input("After logging in, press Enter to save cookies … ")
        save_cookies(driver, path)
        driver.quit()
        print(f"Cookies saved to {path}")


def download_profiles(
    urls: List[str],
    out_dir: Path,
    headless: bool,
    workers: int,
    cookie_path: str,
) -> None:
    """Download every media item from each Threads profile in *urls*.

    Parameters
    ----------
    urls
        A list of Threads profile URLs.
    out_dir
        Destination folder for all downloaded files.
    headless
        When *True*, Chrome runs in headless mode.
    workers
        Number of concurrent download workers.
    cookie_path
        Path to the cookies file that should be loaded before scraping.
    """
    driver = build_stealth_driver(headless=headless)
    driver.get("https://www.threads.net/")
    load_cookies(driver, cookie_path)

    for url in urls:
        driver.get(url)
        author: str = get_author_name(driver)
        print(f"Downloading {author} …")
        media: List[str] = collect_all_media(driver)

        target: Path = out_dir / author
        target.mkdir(parents=True, exist_ok=True)

        batch_download(media, target, workers)
        
    print("All downloads complete!")
    driver.quit()


def ask_yes_no(prompt: str, default: bool = False) -> bool:
    """Return *True* or *False* from a Y/N prompt.

    The default value is returned when the user presses **Enter**
    without typing an answer.
    """
    default_str: str = "Y/n" if default else "y/N"
    while True:
        ans: str = input(f"{prompt} ({default_str}): ").strip().lower()
        if ans == "":
            return default
        if ans in {"y", "yes"}:
            return True
        if ans in {"n", "no"}:
            return False
        print("Please enter y or n.")


def ask_int(prompt: str, default: int) -> int:
    """Return an integer provided by the user or *default* on empty input."""
    while True:
        ans: str = input(f"{prompt} [{default}]: ").strip()
        if ans == "":
            return default
        if ans.isdigit():
            return int(ans)
        print("Please enter a valid integer.")


def main() -> None:
    """Entry-point for the CLI application."""
    print("=" * 30)
    print("Threads Downloader")
    print("=" * 30)

    # Collect profile URLs.
    urls: List[str] = []
    while True:
        url: str = input("Enter a Threads profile URL (blank to finish): ").strip()
        if not url:
            break
        urls.append(url)

    if not urls:
        print("No URLs entered – exiting.")
        return

    # Collect runtime parameters.
    out_dir: Path = Path(
        input(f"Download folder [{DOWNLOAD_FOLDER}]: ").strip() or DOWNLOAD_FOLDER
    )
    headless: bool = ask_yes_no(
        "Run Chrome headless?", default=IS_HEADLESS
    )
    workers: int = ask_int("Concurrent downloads", default=DL_WORKERS)
    cookie_path: str = input(
        "Cookie file path [cookies.pkl]: "
    ).strip() or "cookies.pkl"

    ensure_cookies(cookie_path)
    download_profiles(urls, out_dir, headless, workers, cookie_path)


if __name__ == "__main__":
    main()