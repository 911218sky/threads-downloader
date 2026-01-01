from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import local
from typing import List, Optional, Tuple
import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .utils import get_file_extension, random_uuid

MediaWithGroup = Tuple[str, Optional[int]]

# Realistic browser User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
]

# Accept-Language variations
ACCEPT_LANGUAGES = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.9,en-US;q=0.8",
    "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
]

# Thread-local storage for per-thread sessions
_thread_local = local()


def _get_random_headers() -> dict:
    """Generate randomized browser-like headers."""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,video/*,*/*;q=0.8",
        "Accept-Language": random.choice(ACCEPT_LANGUAGES),
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "image",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "cross-site",
        "Sec-CH-UA": '"Chromium";v="131", "Not_A Brand";v="24"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "DNT": "1",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }


def _get_session() -> requests.Session:
    """Get or create a thread-local session with connection pooling and retry."""
    if not hasattr(_thread_local, "session"):
        sess = requests.Session()
        sess.headers.update(_get_random_headers())
        # Connection pooling: increase pool size for better concurrency
        adapter = HTTPAdapter(
            pool_connections=20,
            pool_maxsize=20,
            max_retries=Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
        )
        sess.mount("https://", adapter)
        sess.mount("http://", adapter)
        _thread_local.session = sess
    return _thread_local.session


def _download_one(url: str, folder: Path, group: Optional[int]) -> bool:
    """Download a single media file to *folder*. Returns True on success."""
    sess = _get_session()
    suffix = get_file_extension(url)
    name = f"{group}_{random_uuid()}.{suffix}" if group is not None else f"{random_uuid()}.{suffix}"
    path = folder / name
    try:
        r = sess.get(url, timeout=20, stream=True)
        r.raise_for_status()
        with path.open("wb") as fp:
            for chunk in r.iter_content(128 << 10):  # 128KB chunks for better throughput
                if chunk:
                    fp.write(chunk)
        return True
    except Exception as exc:
        print(f"\nDownload failed {url}: {exc}")
        return False


def batch_download(
    media: List[MediaWithGroup], folder: Path | str, workers: int = 10
) -> None:
    """Download every URL in *media* concurrently.

    Args:
        media: List of ``(url, group_index)`` pairs.
        folder: Destination directory.
        workers: Thread pool size (default 10 for better throughput).
    """
    # Convert to list if needed to avoid iterator exhaustion
    media_list = list(media) if not isinstance(media, list) else media
    total = len(media_list)
    
    if total == 0:
        print("No media to download.")
        return
    
    tgt = Path(folder)
    tgt.mkdir(parents=True, exist_ok=True)
    
    done = 0
    failed = 0
    
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {pool.submit(_download_one, u, tgt, g): u for u, g in media_list}
        for fut in as_completed(futs):
            if fut.result():
                done += 1
            else:
                failed += 1
            print(f"\rProgress {done + failed}/{total} ({(done + failed)/total:.1%}) | Success: {done} | Failed: {failed}", end="", flush=True)
    
    print(f"\nCompleted: {done} downloaded, {failed} failed.")