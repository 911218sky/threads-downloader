import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth

UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/17.1 Safari/605.1.15",
]

def build_stealth_driver(headless: bool = True) -> webdriver.Chrome:
    """Return a ChromeDriver instance patched to evade basic bot detection.

    Args:
        headless: Launch Chrome in headless mode when ``True``.

    Returns:
        A fully initialised ``webdriver.Chrome`` object ready for navigation.
    """
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")

    opts.add_argument('--log-level=3')
    opts.add_argument('--disable-logging')
    opts.add_argument('--silent-debugger-extension-api')
    
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")

    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    opts.add_argument(f"--user-agent={random.choice(UA_POOL)}")

    service = Service(log_path=os.devnull)
    driver = webdriver.Chrome(service=service, options=opts)
    
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});"},
    )

    stealth(
        driver,
        languages=["zh-TW", "zh", "en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL",
        fix_hairline=True,
    )
    
    return driver