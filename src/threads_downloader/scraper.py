import time
from typing import List, Optional, Set, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver

from .config import SCROLL_PAUSE, IS_DOWNLOAD_IMAGE, IS_DOWNLOAD_VIDEO
from .utils import normalize_url

MediaWithGroup = Tuple[str, Optional[int]]

def get_author_name(drv: WebDriver) -> str:
    """Return the display name of the current Threads profile."""
    return drv.find_element(By.CSS_SELECTOR, ".xcrlgei h1").text.strip()

def _extract_media_src(
    block: WebElement, group: int
) -> Tuple[Set[MediaWithGroup], Set[MediaWithGroup]]:
    """Pull ``src`` attributes for img / video tags inside one post block.

    Args:
        block: The WebElement representing a single Threads post.
        group: Index representing the post order; used in filenames.

    Returns:
        Two sets containing image URLs and video URLs respectively.
    """
    img_xpath = './/*[@referrerpolicy="origin-when-cross-origin"]'
    vid_css = "[playsinline]"
    imgs = {(el.get_attribute("src"), group) for el in block.find_elements(By.XPATH, img_xpath)}
    vids = {(el.get_attribute("src"), group) for el in block.find_elements(By.CSS_SELECTOR, vid_css)}
    return imgs, vids

def collect_all_media(
    drv: WebDriver, pause: float = SCROLL_PAUSE, max_no_change: int = 5
) -> List[MediaWithGroup]:
    """Scroll until no new content loads, aggregating every unique media URL.

    Args:
        drv: An already navigated Selenium driver.
        pause: Seconds to wait between scrolls.
        max_no_change: Stop after this many consecutive scrolls yield no
            height delta.

    Returns:
        A list of ``(url, group_index)`` tuples ready for download.
    """
    seen: Set[str] = set()
    media: List[MediaWithGroup] = []
    last_height = drv.execute_script("return document.body.scrollHeight")
    no_change = 0
    group = 0

    while True:
        for blk in drv.find_elements(By.CLASS_NAME, "x1xmf6yo"):
            imgs, vids = _extract_media_src(blk, group)
            for url, g in (imgs if IS_DOWNLOAD_IMAGE else set()) | (vids if IS_DOWNLOAD_VIDEO else set()):
                key = normalize_url(url)
                if url and key not in seen:
                    seen.add(key)
                    media.append((url, g))
                    group += 1

        drv.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)

        new_height = drv.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            no_change += 1
            if no_change >= max_no_change:
                break
        else:
            last_height = new_height
            no_change = 0
        
        print(f"\rCollected {len(media)} media", end="", flush=True)
        
    # Newline
    print()
    
    return media