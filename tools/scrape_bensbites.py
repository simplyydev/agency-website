import requests
from bs4 import BeautifulSoup
import datetime
import uuid
import json

def fetch_bens_bites():
    """
    Fetches latest articles from Ben's Bites Archive.
    Returns a list of dicts matching the Article schema.
    """
    url = "https://bensbites.substack.com/archive"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        
        # Strategy 2: Look for all links to posts
        # Substack posts usually have '/p/' in the URL.
        
        links = soup.find_all('a')
        seen_urls = set()
        
        for link in links:
            href = link.get('href', '')
            if '/p/' in href:
                # Ensure absolute URL
                if not href.startswith('http'):
                    href = f"https://bensbites.substack.com{href}" # Handle relative if needed, mostly absolute though
                
                # Deduplicate in this run
                if href in seen_urls:
                    continue
                seen_urls.add(href)
                
                title = link.get_text(strip=True)
                if not title:
                    continue
                    
                # Filter out likely non-article links if any
                if "comment" in href or "subscriber" in href:
                    continue
                    
                # Date inference is hard on archive list without specific markup.
                # We will default to now, or try to find a date sibling.
                # Often <time> is near.
                published_at = datetime.datetime.now().isoformat()
                
                # Try to find a date nearby (heuristic)
                # Parent -> check for time
                parent = link.parent
                if parent:
                    time_elem = parent.find('time')
                    if not time_elem and parent.parent:
                         time_elem = parent.parent.find('time')
                    
                    if time_elem and time_elem.has_attr('datetime'):
                        published_at = time_elem['datetime']

                article = {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "url": href,
                    "source": "BensBites",
                    "published_at": published_at,
                    "summary": "", 
                    "tags": ["AI", "Newsletter"],
                    "is_saved": False,
                    "fetched_at": datetime.datetime.now().isoformat()
                }
                articles.append(article)
                
        return articles

    except Exception as e:
        print(f"Error fetching Ben's Bites: {e}")
        return []

if __name__ == "__main__":
    data = fetch_bens_bites()
    print(json.dumps(data[:2], indent=2))
