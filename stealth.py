import asyncio
import logging
import random
from dataclasses import dataclass
from typing import Optional, Dict
from contextlib import asynccontextmanager
from playwright.async_api import async_playwright, Page, Browser, BrowserContext, Playwright

# --- SAFE IMPORT BLOCK ---
# We wrap this in try/except so the app doesn't crash if the library is missing
try:
    from playwright_stealth import stealth_async
except ImportError:
    stealth_async = None  # We will handle this gracefully later

# --- Configuration & Telemetry ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [STEALTH] - %(message)s")
logger = logging.getLogger("GhostBrowser")

# --- Domain Models: Browser Profiles ---
@dataclass
class BrowserProfile:
    user_agent: str
    viewport: Dict[str, int]
    locale: str = "en-US"
    timezone: str = "America/New_York"
    cpu_concurrency: int = 8
    device_memory: int = 8  # in GB
    platform: str = "Win32"
    vendor: str = "Google Inc."
    renderer: str = "Intel Iris OpenGL Engine"

    @classmethod
    def create_desktop_chrome(cls) -> 'BrowserProfile':
        return cls(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            platform="Win32"
        )

# --- Service Layer: Human Behavior Engine ---
class Humanizer:
    @staticmethod
    async def jitter(page: Page):
        try:
            for _ in range(random.randint(2, 5)):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                await page.mouse.move(x, y, steps=random.randint(5, 10))
                await asyncio.sleep(random.uniform(0.1, 0.3))
        except Exception:
            pass 

# --- Infrastructure Layer: The Stealth Factory ---
class StealthSession:
    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url

    @asynccontextmanager
    async def create_context(self, profile: BrowserProfile):
        playwright: Optional[Playwright] = None
        browser: Optional[Browser] = None
        context: Optional[BrowserContext] = None
        
        try:
            playwright = await async_playwright().start()
            
            args = [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars"
            ]
            
            browser = await playwright.chromium.launch(
                headless=True,
                args=args,
                proxy={"server": self.proxy_url} if self.proxy_url else None
            )

            context = await browser.new_context(
                user_agent=profile.user_agent,
                viewport=profile.viewport,
                locale=profile.locale,
                timezone_id=profile.timezone,
                device_scale_factor=1,
                has_touch=False
            )

            page = await context.new_page()

            # --- SAFE STEALTH INJECTION ---
            if stealth_async:
                await stealth_async(page)
            else:
                logger.warning("Stealth module not found. Running in standard mode.")

            # Hardware Spoofing (Works even without the library)
            await page.add_init_script(f"""
                Object.defineProperty(navigator, 'hardwareConcurrency', {{ get: () => {profile.cpu_concurrency} }});
                Object.defineProperty(navigator, 'deviceMemory', {{ get: () => {profile.device_memory} }});
                Object.defineProperty(navigator, 'platform', {{ get: () => "{profile.platform}" }});
            """)
            
            yield page

        except Exception as e:
            logger.error(f"Session failed: {e}")
            raise
        finally:
            if context: await context.close()
            if browser: await browser.close()
            if playwright: await playwright.stop()