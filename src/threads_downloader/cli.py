import argparse
import os
from pathlib import Path

from .config import (
    DL_WORKERS,
    DOWNLOAD_FOLDER,
    IS_HEADLESS,
)
from .downloader import batch_download
from .driver import build_stealth_driver
from .scraper import collect_all_media, get_author_name
from .utils import load_cookies, save_cookies

def get_cookies(save_path: str = "cookies.pkl") -> None:
    print("Please log in to Threads in the newly opened browser window. After you have finished logging in, return to this terminal and press Enter to automatically save your cookies.")
    drv = build_stealth_driver(headless=False)
    drv.get("https://www.threads.net/")
    input("After logging in, press Enter to save cookies ...")
    save_cookies(drv, save_path)
    print("Cookies saved to", save_path)
    drv.quit()

def main() -> None:
    """Parse CLI arguments, launch a browser, scrape, and download."""
    ap = argparse.ArgumentParser(description="Fetch media from Threads profiles.")
    ap.add_argument(
        "--profile",
        nargs="+",
        required=True,
        metavar="URL",
        help="One or more profile URLs to scrape",
    )
    ap.add_argument("--out", default=DOWNLOAD_FOLDER, help="Download directory")
    ap.add_argument(
        "--headless", action="store_true",
        default=IS_HEADLESS, help="Run Chrome headless"
    )
    ap.add_argument("--workers", type=int, default=DL_WORKERS, help="Download threads")
    ap.add_argument("--cookies_path", default="cookies.pkl", help="Path to cookies file")
    args = ap.parse_args()

    if not os.path.exists(args.cookies_path):
        get_cookies(args.cookies_path)
        
    drv = build_stealth_driver(args.headless)
    drv.get("https://www.threads.com/")
    load_cookies(drv, args.cookies_path)

    for url in args.profile:
        drv.get(url)

        author = get_author_name(drv)
        print(f"[{author}] Scrolling and collecting media…")
        media = collect_all_media(drv)
        print(f"[{author}] Found {len(media)} media items.")

        out_dir = Path(args.out) / author
        batch_download(media, out_dir, args.workers)
        save_cookies(drv)
    
    drv.quit()

if __name__ == "__main__":
    main()