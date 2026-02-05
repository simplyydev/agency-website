import requests
import datetime
import uuid
import json

def fetch_reddit_ai():
    """
    Fetches latest posts from r/ArtificialInteligence via JSON.
    Returns a list of dicts matching the Article schema.
    """
    url = "https://www.reddit.com/r/ArtificialInteligence/new.json?limit=10"
    headers = {
        "User-Agent": "AntigravityBot/1.0 (by /u/Antigravity)" # Unique UA is required by Reddit
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            print("Reddit Rate Limit Hit")
            return []
        response.raise_for_status()
        
        data = response.json()
        articles = []
        
        for child in data.get('data', {}).get('children', []):
            post = child.get('data', {})
            
            # Skip stickies if desired, but for now include all new
            
            created_utc = post.get('created_utc', 0)
            dt = datetime.datetime.fromtimestamp(created_utc)
            
            article = {
                "id": str(uuid.uuid4()),
                "title": post.get('title'),
                "url": post.get('url'), # External link or reddit link
                "source": "Reddit",
                "published_at": dt.isoformat(),
                "summary": post.get('selftext', '')[:200] + "..." if post.get('selftext') else "",
                "tags": ["Reddit", "AI"],
                "is_saved": False,
                "fetched_at": datetime.datetime.now().isoformat()
            }
            articles.append(article)
            
        return articles

    except Exception as e:
        print(f"Error fetching Reddit: {e}")
        return []

if __name__ == "__main__":
    data = fetch_reddit_ai()
    print(json.dumps(data[:2], indent=2))
