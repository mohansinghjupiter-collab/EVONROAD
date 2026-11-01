#!/usr/bin/env python3
"""Builds news.json (India + Global EV headlines) from Google News RSS.
Uses only the Python standard library. Run by GitHub Actions every few hours."""
import json, re, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone, timedelta

MAX_PER_TAB = 15
MAX_AGE_DAYS = 10

# Headlines must contain at least one of these (case-insensitive)
MUST_HAVE = ["electric", " ev ", " evs", "ev,", "ev:", "e-scooter", "e-bike", "battery", "charging", "tata.ev", "ola electric",
             "ather", "bgauss", "oben", "ampere", "vinfast", "byd", "mahindra be", "xev", "e vitara", "revolt", "ultraviolette"]
# Headlines containing any of these are dropped
BLOCK = ["petrol price", "diesel price", "horoscope", "stock price target", "share price target", "sensex", "nifty", "ipo"]

INDIA_QUERIES = [
    "electric vehicle India",
    "electric scooter India",
    "Tata.ev OR Mahindra BE OR \"Ola Electric\" OR \"Ather Energy\" OR VinFast India",
    "EV charging India OR \"PM E-DRIVE\" OR \"EV policy\" India",
]
UPCOMING_QUERIES = ["upcoming electric car India launch", "upcoming electric scooter India launch", "electric launch date India unveil"]
UPCOMING_WORDS = ["launch", "unveil", "upcoming", "teased", "debut", "reveal", "to arrive", "bookings open"]
GLOBAL_QUERIES = ["electric vehicles", "EV battery technology", "Tesla OR BYD OR Hyundai electric car"]

def feed_url(query, india):
    q = urllib.parse.quote(f"{query} when:7d")
    if india:
        return f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en"
    return f"https://news.google.com/rss/search?q={q}&hl=en&gl=US&ceid=US:en"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (EVonRoad news bot)"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()

def parse(xml_bytes):
    out = []
    root = ET.fromstring(xml_bytes)
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = item.findtext("pubDate")
        src_el = item.find("source")
        source = (src_el.text or "").strip() if src_el is not None else ""
        # Google News appends " - Source" to titles
        if source and title.endswith(" - " + source):
            title = title[: -(len(source) + 3)].strip()
        elif " - " in title and not source:
            title, source = title.rsplit(" - ", 1)
        try:
            when = parsedate_to_datetime(pub).astimezone(timezone.utc)
        except Exception:
            continue
        if title and link:
            out.append({"title": title, "link": link, "source": source or "News", "published": when.isoformat()})
    return out

def relevant(title):
    t = " " + title.lower() + " "
    if any(b in t for b in BLOCK):
        return False
    return any(k in t for k in MUST_HAVE)

def collect(queries, india, extra_words=None):
    seen, items = set(), []
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)
    for q in queries:
        try:
            batch = parse(fetch(feed_url(q, india)))
        except Exception as e:
            print(f"WARN feed failed for '{q}': {e}", file=sys.stderr)
            continue
        for it in batch:
            key = re.sub(r"\W+", "", it["title"].lower())[:60]
            if key in seen or not relevant(it["title"]):
                continue
            if extra_words and not any(w in it["title"].lower() for w in extra_words):
                continue
            if datetime.fromisoformat(it["published"]) < cutoff:
                continue
            seen.add(key)
            items.append(it)
        time.sleep(1)
    items.sort(key=lambda x: x["published"], reverse=True)
    return items[:MAX_PER_TAB]

def main():
    india = collect(INDIA_QUERIES, True)
    world = collect(GLOBAL_QUERIES, False)
    upcoming = collect(UPCOMING_QUERIES, True, UPCOMING_WORDS)
    if not india and not world and not upcoming:
        print("No items fetched; keeping the existing news.json", file=sys.stderr)
        sys.exit(0)   # do not overwrite a good file with an empty one
    data = {"updated": datetime.now(timezone.utc).isoformat(), "india": india, "global": world, "upcoming": upcoming}
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(india)} India + {len(world)} Global + {len(upcoming)} Upcoming headlines")

if __name__ == "__main__":
    main()
