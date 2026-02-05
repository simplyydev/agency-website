import requests
from bs4 import BeautifulSoup
import datetime
import uuid
import json

def fetch_rundown_ai():
    """
    Fetches latest articles from The AI Rundown homepage.
    Returns a list of dicts matching the Article schema.
    """
    url = "https://www.therundown.ai/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        
        # Based on research, "Latest Articles" section.
        # We saw markdown headers in the chunk view: ### Title
        # In HTML, these are likely H3 tags inside a container.
        
        # Strategy: Find all H3s, check if they look like article titles (have links).
        # OR: Look for specific container structure if known. 
        # 'h3' tags seem to be the titles.
        
        candidates = soup.find_all('h3')
        
        for h3 in candidates:
            # Check if wrapped in 'a' or has 'a' sibling/child
            link_elem = h3.find_parent('a') or h3.find('a')
            
            # Sometimes the structure is link -> div -> h3
            if not link_elem:
                # heuristic: check parent's parent
                parent = h3.parent
                if parent and parent.name == 'a':
                    link_elem = parent
            
            if link_elem:
                link = link_elem.get('href')
                if link and link.startswith('/'):
                    link = f"https://www.therundown.ai{link}"
                
                title = h3.get_text(strip=True)
                
                article = {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "url": link,
                    "source": "TheRundown",
                    "published_at": datetime.datetime.now().isoformat(), # Homepage often doesn't have dates easily, default to now
                    "summary": "",
                    "tags": ["AI", "News"],
                    "is_saved": False,
                    "fetched_at": datetime.datetime.now().isoformat()
                }
                articles.append(article)
                
        return articles

    except Exception as e:
        print(f"Error fetching The Rundown: {e}")
        return []

if __name__ == "__main__":
    data = fetch_rundown_ai()
    print(json.dumps(data[:2], indent=2))
