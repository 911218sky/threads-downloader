from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable, Optional, Tuple
import requests
from .utils import get_file_extension, random_uuid

MediaWithGroup = Tuple[str, Optional[int]]

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
    sess.headers.update({"User-Agent": "Mozilla/5.0 Chrome/124 Safari/537.36"})
    total = len(list(media))
    done = 0
    with ThreadPoolExecutor(workers) as pool:
        futs = [pool.submit(_download_one, sess, u, tgt, g) for u, g in media]
        for _ in as_completed(futs):
            done += 1
            print(f"Progress {done}/{total} ({done/total:.1%})", end="\r")