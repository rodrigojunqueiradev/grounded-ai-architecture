"""Render the SVG diagram to the two PNG sizes used by the README and Upwork.

Uses Playwright (Chromium screenshot of an HTML page embedding the SVG),
because cairosvg needs a native cairo DLL that is not available on Windows.

Outputs:
- anti-hallucination-architecture.png (1600x800)
- upwork-thumbnail.png (1000x750, diagram centered with margin)
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
SVG = (HERE / "anti-hallucination-architecture.svg").read_text(encoding="utf-8")
BACKGROUND = "#F8F9FB"

PAGE = """<!doctype html>
<html><head><style>
  * {{ margin: 0; padding: 0; }}
  body {{ width: {w}px; height: {h}px; background: {bg};
         display: flex; align-items: center; justify-content: center; }}
  svg {{ width: {svg_w}px; height: auto; display: block; }}
</style></head><body>{svg}</body></html>"""


def shoot(page, path: Path, width: int, height: int, svg_width: int) -> None:
    page.set_viewport_size({"width": width, "height": height})
    page.set_content(PAGE.format(w=width, h=height, bg=BACKGROUND, svg_w=svg_width, svg=SVG))
    page.screenshot(path=str(path))
    print(f"{path.name}: {width}x{height}")


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(device_scale_factor=1)
        shoot(page, HERE / "anti-hallucination-architecture.png", 1600, 720, 1600)
        shoot(page, HERE / "upwork-thumbnail.png", 1000, 750, 940)
        browser.close()


if __name__ == "__main__":
    main()
