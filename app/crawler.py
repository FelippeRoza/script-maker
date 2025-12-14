import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
from urllib.parse import urljoin
import time

def load_posts(start_url, max_posts=10):
    """Crawl main page, find post-thumbnail links, load their content"""
    
    # Get main page
    print(f"Crawling: {start_url}")
    response = requests.get(start_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find links inside post-thumbnail elements
    article_links = set()
    
    # Target post-thumbnail specifically
    post_thumbnails = soup.find_all('div', class_='post-thumbnail')
    for thumb in post_thumbnails:
        a_tag = thumb.find('a', href=True)
        if a_tag:
            full_url = urljoin(start_url, a_tag['href'])
            article_links.add(full_url)
    
    # Fallback: also check links WITHIN post-thumbnail class
    for a in soup.find_all('a', href=True):
        if 'post-thumbnail' in a.get('class', []):
            full_url = urljoin(start_url, a['href'])
            article_links.add(full_url)
    
    print(f"Found {len(article_links)} post-thumbnail articles")
    
    if not article_links:
        print("No post-thumbnail links found. Showing all links for debugging:")
        all_links = soup.find_all('a', href=True)[:20]
        for link in all_links:
            print(f"  - {link.get('href')}")
    
    # Load content from each article
    docs = []
    for i, url in enumerate(list(article_links)[:max_posts]):
        try:
            print(f"Loading article {i+1}/{min(max_posts, len(article_links))}: {url}")
            loader = WebBaseLoader(url)
            doc = loader.load()[0]
            doc.metadata['source_url'] = url
            docs.append(doc)
            time.sleep(0.1)  # Polite delay
        except Exception as e:
            print(f"Failed to load {url}: {e}")
    
    return docs
