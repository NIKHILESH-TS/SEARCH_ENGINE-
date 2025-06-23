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


        parsed_urls.append(href.split("#")[0])
    return parsed_urls