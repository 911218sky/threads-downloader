from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable, Optional, Tuple
import random
import requests
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

def _download_one(sess: requests.Session, url: str, folder: Path, group: Optional[int]) -> None:
    """Download a single media file to *folder* using *sess*."""
    suffix = get_file_extension(url)
    name = f"{group}_{random_uuid()}.{suffix}" if group is not None else f"{random_uuid()}.{suffix}"
    path = folder / name
    try:
        r = sess.get(url, timeout=15, stream=True)
        r.raise_for_status()
        with path.open("wb") as fp:
            for chunk in r.iter_content(64 << 10):
                if chunk:
                    fp.write(chunk)
    except Exception as exc:
        print(f"Download failed {url}: {exc}")


def batch_download(
    media: Iterable[MediaWithGroup], folder: Path | str, workers: int = 8
) -> None:
    """Download every URL in *media* concurrently.

    Args:
        media: Iterable of ``(url, group_index)`` pairs.
        folder: Destination directory.
        workers: Thread pool size.
    """
    tgt = Path(folder)
    tgt.mkdir(parents=True, exist_ok=True)
    sess = requests.Session()
    sess.headers.update(_get_random_headers())
    total = len(list(media))
    done = 0
    with ThreadPoolExecutor(workers) as pool:
        futs = [pool.submit(_download_one, sess, u, tgt, g) for u, g in media]
        for _ in as_completed(futs):
            done += 1
            print(f"Progress {done}/{total} ({done/total:.1%})", end="\r")