import time
import json
import random
import threading
from queue import Queue
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

# --- Blocked Domains ---
BLOCKED_DOMAINS = {
    # === Social Media ===
    "facebook.com", "instagram.com", "twitter.com", "x.com", "tiktok.com", "snapchat.com",
    "reddit.com", "pinterest.com", "linkedin.com", "tumblr.com", "youtube.com", "vimeo.com",
    "twitch.tv", "clubhouse.com", "discord.com", "telegram.org", "wechat.com", "weibo.com",
    "line.me", "kakao.com", "kakaocorp.com", "threads.net", "bilibili.com", "quora.com",
    "medium.com", "mastodon.social", "gettr.com", "gab.com", "truthsocial.com", "hive.blog",
    "mewe.com", "nextdoor.com", "flickr.com", "imgur.com", "mix.com", "vk.com", "ok.ru",
    "xuite.net", "plurk.com", "coub.com", "tagged.com", "myspace.com", "friendster.com",
    "viadeo.com", "newgrounds.com", "bitclout.com", "ello.co", "peach.cool", "wt.social",
    "spacehey.com", "steemit.com",

    # === Streaming & Entertainment ===
    "netflix.com", "hulu.com", "disneyplus.com", "primevideo.com", "hotstar.com", "zee5.com",
    "sonyliv.com", "crunchyroll.com", "spotify.com", "gaana.com", "jiosaavn.com", "wynk.in",
    "soundcloud.com", "audible.com", "pandora.com", "dailymotion.com",

    # === E-commerce / Marketplaces ===
    "amazon.com", "flipkart.com", "meesho.com", "snapdeal.com", "myntra.com", "ajio.com",
    "ebay.com", "etsy.com", "craigslist.org", "shopify.com", "zappos.com", "shein.com",
    "asos.com", "boohoo.com", "zalando.com", "walmart.com", "bestbuy.com", "target.com",
    "costco.com", "homedepot.com", "lowes.com", "ikea.com", "wayfair.com", "overstock.com",

    # === Real Estate ===
    "zillow.com", "trulia.com", "realtor.com", "magicbricks.com", "99acres.com", "housing.com",

    # === Travel & Booking ===
    "airbnb.com", "booking.com", "expedia.com", "tripadvisor.com", "hotels.com", "kayak.com",
    "skyscanner.com", "orbitz.com", "travelocity.com", "priceline.com", "makemytrip.com",
    "goibibo.com", "cleartrip.com", "agoda.com", "ixigo.com",

    # === Airlines ===
    "southwest.com", "delta.com", "united.com", "americanairlines.com", "jetblue.com",
    "alaskaair.com", "virginamerica.com", "spirit.com", "frontierairlines.com", "ryanair.com",
    "easyjet.com", "lufthansa.com", "britishairways.com", "airfrance.com", "klm.com",
    "emirates.com", "qatarairways.com", "indigo.com", "vistara.com", "airindia.com",

    # === Crowdfunding & Activism ===
    "patreon.com", "kickstarter.com", "indiegogo.com", "gofundme.com", "crowdfunder.com",
    "crowdsupply.com", "seedrs.com", "crowdcube.com", "fundable.com", "startsomegood.com",
    "fundrazr.com", "change.org", "avaaz.org", "moveon.org", "care2.com", "actionnetwork.org",
    "sumofus.org", "greenpeace.org", "wwf.org", "amnesty.org", "humanrightsfirst.org",
    "hrw.org", "icrc.org",

    # === Government & Global Organizations ===
    "unicef.org", "who.int", "un.org", "worldbank.org", "imf.org", "oecd.org", "europa.eu",
    "nato.int", "cia.gov", "fbi.gov", "usps.com", "irs.gov", "nasa.gov", "whitehouse.gov",
    "gov.uk", "gov.in",

    # === Search Engines & Portals ===
    "google.com", "bing.com", "yahoo.com", "baidu.com", "yandex.ru", "duckduckgo.com", 
    "wikipedia.org",

    # === Tech/Code Hosting ===
    "github.com", "gitlab.com", "bitbucket.org",

    # === Chinese Marketplaces & Portals ===
    "alibaba.com", "taobao.com", "tmall.com", "jd.com", "qq.com", "sina.com.cn", "sohu.com",
    "163.com"
}# (unchanged for brevity)

# --- Retryable Fetch ---
def fetch_with_retries(url, headers=None, retries=3, timeout=10, backoff=2):
    for i in range(retries):
        try:
            return requests.get(url, headers=headers, timeout=timeout)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            print(f"[RETRY {i+1}] {url} failed: {e}")
            time.sleep(backoff * (i + 1))  # Exponential backoff
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Unrecoverable error for {url}: {e}")
            break
    return None

# --- Robots.txt checker ---
def can_crawl(url):
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    print(f"[INFO] Checking robots.txt: {robots_url}")
    time.sleep(random.uniform(1, 3))
    headers = {"User-Agent": "Mozilla/5.0"}
    res = fetch_with_retries(robots_url, headers=headers, timeout=5)
    if not res:
        print(f"[WARNING] Couldn't retrieve robots.txt. Defaulting to allowed.")
        return True

    disallowed = [line.split(':')[1].strip() for line in res.text.splitlines()
                  if line.lower().startswith('disallow') and ':' in line]
    path = parsed.path or "/"
    for dis_path in disallowed:
        if path.startswith(dis_path):
            print(f"[BLOCKED] {url} disallowed by robots.txt")
            return False
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

        parsed_domain = urlparse(href).netloc.lower()
        if any(blocked in parsed_domain for blocked in BLOCKED_DOMAINS):
            continue  # Skip blocked domains

        parsed_urls.append(href.split("#")[0])
    return parsed_urls

# --- Enhanced Page Indexer ---
def simple_index_page(soup, url):
    title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"
    description_tag = soup.find("meta", attrs={"name": "description"})
    description = description_tag["content"].strip() if description_tag and description_tag.get("content") else "No Description"

    # Try to find author and date
    author = "Unknown"
    author_tag = soup.find("meta", attrs={"name": "author"})
    if author_tag and author_tag.get("content"):
        author = author_tag["content"].strip()
    elif soup.find(class_="author"):
        author = soup.find(class_="author").get_text(strip=True)

    date = "Unknown"
    for time_tag in soup.find_all("time"):
        if time_tag.get("datetime"):
            date = time_tag["datetime"]
            break
        elif time_tag.get_text(strip=True):
            date = time_tag.get_text(strip=True)
            break

    words = set(word.lower() for word in soup.get_text().split())
    return {
        "url": url,
        "title": title,
        "description": description,
        "author": author,
        "date": date,
        "words": words
    }

# --- Worker Thread Function ---
def crawl(args):
    queue, visited, count, limit, lock, index, info, doc_id, stop, output_file = (
        args['queue'], args['visited'], args['count'], args['limit'],
        args['lock'], args['index'], args['info'], args['doc_id'], args['stop'], args['output_file'])

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    while not stop.is_set():
        try:
            url = queue.get(timeout=5)
        except Exception:
            break

        domain = urlparse(url).netloc.lower()
        if any(blocked in domain for blocked in BLOCKED_DOMAINS):
            print(f"[SKIP] Blocked domain: {url}")
            queue.task_done()
            continue

        with lock:
            if count[0] >= limit:
                queue.queue.clear()
                stop.set()
                print("[INFO] Crawl limit reached.")
                break
            if url in visited:
                queue.task_done()
                continue
            visited.add(url)

        print(f"[CRAWL] Fetching: {url}")
        time.sleep(random.uniform(2, 5))
        res = fetch_with_retries(url, headers=headers, retries=3, timeout=10)

        if not res or res.status_code != 200:
            print(f"[ERROR] Giving up on {url}")
            queue.task_done()
            continue

        try:
            soup = BeautifulSoup(res.content, "html.parser")
            result = simple_index_page(soup, url)

            with lock:
                current_doc_id = doc_id[0]

                doc_data = {
                    'doc_id': current_doc_id,
                    'url': result['url'],
                    'title': result['title'],
                    'description': result['description'],
                    'author': result['author'],
                    'date': result['date']
                }

                output_file.write(json.dumps(doc_data, ensure_ascii=False) + '\n')

                for word in result["words"]:
                    index.setdefault(word, set()).add(current_doc_id)
                info[current_doc_id] = result
                doc_id[0] += 1

            new_links = parse_links(soup.select("a[href]"), url)
            with lock:
                for link in new_links:
                    if link not in visited:
                        queue.put(link)
                count[0] += 1

        except Exception as e:
            print(f"[ERROR] Processing failed for {url}: {e}")
        finally:
            queue.task_done()

# --- Main Bot Logic ---
def starck_bot():
    seeds = [
        "https://example.com",]

    q = Queue()
    for url in seeds:
        q.put(url)

    visited = set()
    limit = 4000
    count = [0]
    lock = threading.Lock()
    index, info = {}, {}
    doc_id = [0]
    stop = threading.Event()

    output_filename = 'data.jsonl'
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        args = {
            'queue': q,
            'visited': visited,
            'count': count,
            'limit': limit,
            'lock': lock,
            'index': index,
            'info': info,
            'doc_id': doc_id,
            'stop': stop,
            'output_file': output_file
        }

        NUM_THREADS = 100
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            for _ in range(NUM_THREADS):
                executor.submit(crawl, args)

    print(f"[INFO] Crawling completed. Data saved to {output_filename}")

# --- Entrypoint ---
def main():
    starck_bot()

if __name__ == "__main__":
    main()