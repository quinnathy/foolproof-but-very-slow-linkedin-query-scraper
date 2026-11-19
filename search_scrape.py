# pip install playwright && playwright install chromium
# python search_scrape.py        (start at page 1)
# python search_scrape.py 2 5    (get pages 2 - 5 inclusive)
# python search_scrape.py 25     (resume from page 25)
import csv, random, re, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = (
    # YOUR LINKEDIN SEARCH URL GOES HERE
    )

OUT = Path("profiles.csv")
START_PAGE = int(sys.argv[1]) if len(sys.argv) > 1 else 1
MAX_PAGE = int(sys.argv[2]) if len(sys.argv) > 2 else 100
PAGE_TIME = (28, 38)        # seconds per page (randomized)

def clean(url):
    m = re.match(r"(https://www\.linkedin\.com/in/[^/?#]+)", url)
    return m.group(1) if m else None

# For each profile link, walk up the DOM until the container would include a
# second distinct profile; the last container before that is the result card.
EXTRACT_JS = """
els => {
  const prof = h => { const m = (h||'').match(/linkedin\\.com\\/in\\/[^\\/?#]+/); return m ? m[0] : null; };
  return els.map(a => {
    const me = prof(a.href);
    let node = a, best = a;
    for (let i = 0; i < 8 && node.parentElement; i++) {
      node = node.parentElement;
      const others = new Set(
        [...node.querySelectorAll('a[href*="/in/"]')].map(x => prof(x.href)).filter(p => p && p !== me)
      );
      if (others.size > 0) break;
      best = node;
    }
    return {href: a.href, text: (best.innerText || '').replace(/\\s+/g, ' ').trim()};
  });
}
"""

seen = set()
if OUT.exists():
    with OUT.open(newline="") as f:
        seen = {row[0] for row in csv.reader(f) if row}

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    ctx = browser.contexts[0]
    page = ctx.new_page()

    page.goto("https://www.linkedin.com/feed/")
    if any(s in page.url for s in ("login", "authwall", "checkpoint")):
        input("Log in to LinkedIn in the browser window, then press Enter here...")

    empty_streak = 0
    with OUT.open("a", newline="") as f:
        w = csv.writer(f)
        if f.tell() == 0:
            w.writerow(["profile_url", "page", "card_text"])

        for n in range(START_PAGE, MAX_PAGE + 1):
            t0 = time.time()
            budget = random.uniform(*PAGE_TIME)
            page.goto(f"{BASE}&page={n}", wait_until="domcontentloaded")

            if any(s in page.url for s in ("checkpoint", "authwall", "login")):
                print(f"Challenge/logout at page {n}. Stopping; resume with: python scrape.py {n}")
                break

            # scroll gradually so lazy-loaded results render
            for _ in range(random.randint(5, 8)):
                page.mouse.wheel(0, random.randint(400, 800))
                page.wait_for_timeout(random.randint(1200, 2500))

            cards = page.eval_on_selector_all('a[href*="/in/"]', EXTRACT_JS)

            rows = {}
            for c in cards:
                u = clean(c["href"])
                if u and (u not in rows or len(c["text"]) > len(rows[u])):
                    rows[u] = c["text"]

            new = 0
            for u, text in rows.items():
                if u in seen:
                    continue
                seen.add(u)
                new += 1
                w.writerow([u, n, text[:300]])
            f.flush()
            print(f"Page {n}: {len(rows)} found, {new} new")

            empty_streak = empty_streak + 1 if not rows else 0
            if empty_streak >= 2:
                print("No more results. Done.")
                break

            remaining = budget - (time.time() - t0)
            if remaining > 0:
                time.sleep(remaining)
            if n % 5 == 0:
                pause = random.uniform(120, 300)
                print(f"Taking a {pause/60:.1f} min break...")
                time.sleep(pause)

    page.close() 