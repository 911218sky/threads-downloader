import os
import pickle
import pathlib
from typing import Any
from urllib.parse import urlparse
import uuid_utils as uuid

def save_cookies(driver, file_path: str = "cookies.pkl") -> None:
    """Persist Selenium cookies to disk so later runs stay logged-in."""
    with open(file_path, "wb") as f:
        pickle.dump(driver.get_cookies(), f)


def load_cookies(driver, file_path: str = "cookies.pkl") -> None:
    """Inject previously saved cookies into a driver session if available."""
    if not pathlib.Path(file_path).exists():
        return
    with open(file_path, "rb") as f:
        for ck in pickle.load(f):
            driver.add_cookie(ck)
    driver.refresh()


def dump_pickle(data: Any, file_path: str) -> None:
    """Serialize *data* into a pickle file located at *file_path*."""
    with open(file_path, "wb") as f:
        pickle.dump(data, f)


def load_pickle(file_path: str) -> Any:
    """Deserialize an object previously written by :func:`dump_pickle`."""
    with open(file_path, "rb") as f:
        return pickle.load(f)


def normalize_url(url: str) -> str:
    """Strip query / fragment parts and return the basename of *url*."""
    return os.path.basename(urlparse(url).path)


def get_file_extension(url: str) -> str:
    """Return the file extension (without dot) or ``'file'`` when absent."""
    ext = pathlib.Path(urlparse(url).path).suffix
    return ext.lstrip(".") or "file"

def random_uuid() -> str:
    """Generate a time-sortable UUIDv7 string for unique filenames."""
    return str(uuid.uuid7())