import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urlparse

def AshStark_7():
    """
    A simple and polite web crawler that crawls a limited number of web pages
    starting from a seed URL. The crawler collects hyperlinks from each visited page,
    converts them into absolute URLs, and continues visiting newly discovered links.
    """

    # Initial list of URLs to begin crawling
    urls_to_visit = ["https://en.wikipedia.org/wiki/Google"]
    visited_urls = set()

    # Maximum number of pages to crawl
    MAX_CRAWL_LIMIT = 15
    crawl_count = 0

    # Start timing the crawl process
    start_time = time.time()

    while urls_to_visit and crawl_count < MAX_CRAWL_LIMIT:
        current_url = urls_to_visit.pop(0)
        print(f"[{crawl_count + 1}] Crawling: {current_url}")

        # Introduce a short delay to avoid overwhelming servers
        time.sleep(random.uniform(1, 3))

        try:
            response = requests.get(current_url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to retrieve {current_url}: {e}")
            continue

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract all hyperlink elements
        for link in soup.select("a[href]"):
            href = link["href"]

            # Skip same-page anchors
            if href.startswith("#"):
                continue

            # Convert relative or protocol-relative links to absolute URLs
            if href.startswith("//"):
                href = "https:" + href
            elif href.startswith("/"):
                parsed_url = urlparse(current_url)
                href = f"{parsed_url.scheme}://{parsed_url.netloc}{href}"
            elif not href.startswith("http"):
                continue

            # Remove URL fragments (e.g., #section)
            href = href.split("#")[0]

            # Add new URL to the queue if not already visited
            if href not in visited_urls:
                urls_to_visit.append(href)
                visited_urls.add(href)

        crawl_count += 1

    elapsed_time = time.time() - start_time
    print(f"\nCrawling completed. {crawl_count} pages visited in {elapsed_time:.2f} seconds.")

def main():
    AshStark_7()

if __name__ == "__main__":
    main()
