import time
import random
import requests
from urllib.parse import urlparse


# --- Robots.txt checker ---
def can_crawl(url):
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    print(f"[INFO] Checking robots.txt: {robots_url}")
    time.sleep(random.uniform(1, 3))
    try:
        res = requests.get(robots_url, timeout=5)
        res.raise_for_status()
        disallowed = [line.split(':')[1].strip() for line in res.text.splitlines()
                      if line.lower().startswith('disallow') and ':' in line]
        path = parsed.path or "/"
        for dis_path in disallowed:
            if path.startswith(dis_path):
                print(f"[BLOCKED] {url} disallowed by robots.txt")
                return False
        return True
    except requests.RequestException as e:
        print(f"[WARNING] Couldn't retrieve robots.txt ({e}). Defaulting to allowed.")
        return True
    
# --- Blocked Domains ---
BLOCKED_DOMAINS = {"google.com", "youtube.com", "facebook.com", "twitter.com", "instagram.com", "linkedin.com", "pinterest.com", "tiktok.com", "reddit.com", "snapchat.com", "tumblr.com", "wikipedia.org", "yahoo.com", "bing.com", "baidu.com", "yandex.ru", "vk.com", "qq.com", "weibo.com", "naver.com", "daum.net", "sina.com.cn", "sohu.com", "163.com", "alibaba.com", "jd.com", "taobao.com", "tmall.com", "amazon.com", "ebay.com", "etsy.com", "craigslist.org", "walmart.com", "bestbuy.com", "target.com", "costco.com", "homedepot.com", "lowes.com", "ikea.com", "wayfair.com", "overstock.com", "zillow.com", "trulia.com", "realtor.com", "airbnb.com", "booking.com", "expedia.com", "tripadvisor.com", "hotels.com", "kayak.com", "skyscanner.com", "orbitz.com", "travelocity.com", "priceline.com", "southwest.com", "delta.com", "united.com", "americanairlines.com", "jetblue.com", "alaskaair.com", "virginamerica.com", "spirit.com", "frontierairlines.com", "ryanair.com", "easyjet.com", "lufthansa.com", "britishairways.com", "airfrance.com", "klm.com", "emirates.com", "qatarairways.com","patreon.com", "kickstarter.com", "indiegogo.com", "gofundme.com", "crowdfunder.com", "crowdsupply.com", "seedrs.com", "crowdcube.com", "fundable.com", "startsomegood.com", "fundrazr.com", "change.org", "avaaz.org", "moveon.org", "care2.com", "actionnetwork.org", "sumofus.org", "greenpeace.org", "wwf.org", "amnesty.org", "humanrightsfirst.org", "hrw.org", "icrc.org", "unicef.org", "who.int", "un.org", "worldbank.org", "imf.org", "oecd.org", "europa.eu", "nato.int", "cia.gov", "fbi.gov", "usps.com"}

# --- HTML Link Parser ---
def parse_links(hyperlinks, base_url):
    parsed_urls = []
    base = urlparse(base_url)
    for tag in hyperlinks:
        href = tag.get("href")
        if not href or href.startswith("#"):
            continue
        if href.startswith("//"):
            href = f"https:{href}"
        elif href.startswith("/"):
            href = f"{base.scheme}://{base.netloc}{href}"
        elif not href.startswith("http"):
            continue

        parsed_domain = urlparse(href).netloc.lower()
        if any(blocked in parsed_domain for blocked in BLOCKED_DOMAINS):
            continue  # Skip blocked domains

        parsed_urls.append(href.split("#")[0])
    return parsed_urls
