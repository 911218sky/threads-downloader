import time
from typing import List, Optional, Set, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException

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
    try:
        imgs = {(el.get_attribute("src"), group) for el in block.find_elements(By.XPATH, img_xpath)}
        vids = {(el.get_attribute("src"), group) for el in block.find_elements(By.CSS_SELECTOR, vid_css)}
    except StaleElementReferenceException:
        return set(), set()
    return imgs, vids


def _check_end_of_content(drv: WebDriver) -> bool:
    """Check if page shows 'no more content' indicator."""
    end_texts = ['沒有更多', '没有更多', 'No more', "You've seen all", '已經看完', '已经看完']
    try:
        page_text = drv.find_element(By.TAG_NAME, "body").text
        return any(text in page_text for text in end_texts)
    except:
        return False


def collect_all_media(
    drv: WebDriver, pause: float = SCROLL_PAUSE, max_no_change: int = 3
) -> List[MediaWithGroup]:
    """Scroll until no new content loads, aggregating every unique media URL.

    Args:
        drv: An already navigated Selenium driver.
        pause: Seconds to wait between scrolls.
        max_no_change: Stop after this many consecutive scrolls yield no
            new content.

    Returns:
        A list of ``(url, group_index)`` tuples ready for download.
    """
    import random
    
    seen_urls: Set[str] = set()
    media: List[MediaWithGroup] = []
    last_media_count = 0
    last_scroll_pos = 0
    no_change = 0
    group = 0

    while True:
        blocks = drv.find_elements(By.CLASS_NAME, "x1xmf6yo")
        
        for blk in blocks:
            imgs, vids = _extract_media_src(blk, group)
            collected_any = False
            
            media_set = set()
            if IS_DOWNLOAD_IMAGE:
                media_set |= imgs
            if IS_DOWNLOAD_VIDEO:
                media_set |= vids
            
            for url, g in media_set:
                if not url:
                    continue
                key = normalize_url(url)
                if key not in seen_urls:
                    seen_urls.add(key)
                    media.append((url, g))
                    collected_any = True
            
            if collected_any:
                group += 1

        # Human-like scroll: random distance between 70-90% of viewport
        scroll_percent = random.uniform(0.7, 0.9)
        drv.execute_script(f"""
            window.scrollBy({{
                top: window.innerHeight * {scroll_percent},
                behavior: 'smooth'
            }});
        """)
        time.sleep(pause + random.uniform(-0.2, 0.3))

        current_media_count = len(media)
        current_scroll_pos = drv.execute_script("return window.pageYOffset")
        
        # Multi-condition end detection:
        # 1. Check if at bottom of page
        scroll_top = drv.execute_script("return window.pageYOffset + window.innerHeight")
        scroll_height = drv.execute_script("return document.body.scrollHeight")
        at_bottom = scroll_top >= scroll_height - 10
        
        # 2. Check if scroll position stopped changing (can't scroll further)
        scroll_stuck = current_scroll_pos == last_scroll_pos
        
        # 3. Check if no new media found
        no_new_media = current_media_count == last_media_count
        
        # 4. Check for "no more content" UI indicator
        end_marker_found = _check_end_of_content(drv)
        
        # End immediately if UI says no more content
        if end_marker_found and no_new_media:
            print(f"\rCollected {len(media)} media (end of content)", end="", flush=True)
            break
        
        # Increment no_change only when multiple conditions met
        if no_new_media and (at_bottom or scroll_stuck):
            no_change += 1
            if no_change >= max_no_change:
                break
        else:
            no_change = 0
        
        last_media_count = current_media_count
        last_scroll_pos = current_scroll_pos

        print(f"\rCollected {len(media)} media", end="", flush=True)

    print()
    return media