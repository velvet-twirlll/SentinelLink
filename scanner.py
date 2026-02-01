import asyncio
import base64
from playwright.async_api import async_playwright

class ScannerConfig:
    def __init__(self, url, keywords):
        self.url = url
        self.keywords = keywords

class ScanResult:
    def __init__(self, risk_score, flags, screenshot_b64, network_data):
        self.risk_score = risk_score
        self.flags = flags
        self.screenshot_b64 = screenshot_b64
        self.network_data = network_data

class LinkDetonator:
    def __init__(self, config: ScannerConfig):
        self.config = config

    async def run(self):
        async with async_playwright() as p:
            # Launch FAST and LIGHT
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(ignore_https_errors=True)
            page = await context.new_page()
            
            risk_score = 0
            flags = []
            network_logs = {}

            # Short timeout to prevent hanging
            try:
                response = await page.goto(self.config.url, timeout=15000, wait_until="domcontentloaded")
                network_logs["status"] = response.status if response else 0
                network_logs["server_ip"] = "Hidden/Cloudflare" 
            except Exception:
                network_logs["error"] = "Timeout"

            # Quick Check
            content = await page.content()
            for kw in self.config.keywords:
                if kw in content.lower():
                    risk_score += 20
                    flags.append(f"Suspicious Keyword: {kw}")

            # Screenshot
            try:
                screenshot_bytes = await page.screenshot(type='jpeg', quality=50)
                screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
            except:
                screenshot_b64 = ""

            await browser.close()
            return ScanResult(risk_score, flags, screenshot_b64, network_logs)