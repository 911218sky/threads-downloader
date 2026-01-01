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
        cookies = pickle.load(f)
    
    # Get current domain
    current_url = driver.current_url
    current_domain = urlparse(current_url).netloc
    
    for ck in cookies:
        try:
            # Try to match cookie domain with current domain
            cookie_domain = ck.get('domain', '')
            if cookie_domain:
                # Remove leading dot from domain
                clean_cookie_domain = cookie_domain.lstrip('.')
                clean_current_domain = current_domain.lstrip('.')
                
                # Skip if domains don't match (threads.net vs threads.com)
                if clean_cookie_domain not in clean_current_domain and clean_current_domain not in clean_cookie_domain:
                    continue
            
            driver.add_cookie(ck)
        except Exception:
            # Skip invalid cookies
            pass
    
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
    """Strip query / fragment parts and return the basename of the URL."""
    return os.path.basename(urlparse(url).path)


def get_file_extension(url: str) -> str:
    """Return the file extension (without dot) or ``'file'`` when absent."""
    ext = pathlib.Path(urlparse(url).path).suffix
    return ext.lstrip(".") or "file"

def random_uuid() -> str:
    """Generate a time-sortable UUIDv7 string for unique filenames."""
    return str(uuid.uuid7())