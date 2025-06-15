from playwright.sync_api import sync_playwright
import os

def scrape_chapter(url, output_dir="output", chapter_name="chapter1"):
    os.makedirs(output_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print(f"[+] Navigating to {url}")
        page.goto(url, wait_until="networkidle")

        # Screenshot
        screenshot_path = os.path.join(output_dir, f"{chapter_name}.png")
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"[OK] Screenshot saved to {screenshot_path}")

        # Extract text
        content_selector = "#mw-content-text"
        content_text = page.locator(content_selector).inner_text()

        # Save text
        text_path = os.path.join(output_dir, f"{chapter_name}.txt")
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(content_text)
        print(f"[OK] Text content saved to {text_path}")

        browser.close()

# Entry point when called by subprocess
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python scrapper.py <url> <chapter_name>")
        exit(1)
    scrape_chapter(sys.argv[1], "output", sys.argv[2])
