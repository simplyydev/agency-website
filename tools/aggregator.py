import json
import os
import uuid
import datetime
import concurrent.futures

# Import scrapers
from scrape_bensbites import fetch_bens_bites
from scrape_rundown import fetch_rundown_ai
from scrape_reddit import fetch_reddit_ai

# Configuration
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(TOOLS_DIR, "../data")
OUTPUT_FILE = os.path.join(DATA_DIR, "articles.json")

def load_existing_articles():
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r') as f:
                return json.load(f).get('articles', [])
        except Exception as e:
            print(f"Error loading existing articles: {e}")
            return []
    return []

def save_articles(articles):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    data = {"last_fetch": datetime.datetime.now().isoformat(), "articles": articles}
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(articles)} articles to {OUTPUT_FILE}")

def run_aggregation():
    print("Starting aggregation...")
    
    existing_articles = load_existing_articles()
    existing_urls = {a['url'] for a in existing_articles}
    
    new_articles = []
    
    # Run scrapers in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(fetch_bens_bites): "BensBites",
            executor.submit(fetch_rundown_ai): "TheRundown",
            executor.submit(fetch_reddit_ai): "Reddit"
        }
        
        for future in concurrent.futures.as_completed(futures):
            source = futures[future]
            try:
                results = future.result()
                print(f"Fetched {len(results)} from {source}")
                for article in results:
                    if article['url'] not in existing_urls:
                        new_articles.append(article)
                        existing_urls.add(article['url'])
            except Exception as e:
                print(f"Error in {source} scraper: {e}")
                
    # Combine and Sort
    # Logic: Keep old articles + new articles. 
    # BUT user said "run every 24 hours. new data, show them. if invalid, forget about it."
    # And "saved articles should be there".
    # Implementation: 
    # 1. Identify "Saved" articles from existing list.
    # 2. Keep Saved articles.
    # 3. Add New articles.
    # 4. Maybe keep unsaved recent articles? For now, we'll keep all unique articles, 
    #    and let the frontend filter by date/saved status if needed. 
    #    Actually, user said "Last 24 hours".
    
    combined = existing_articles + new_articles
    
    # Sort by published_at desc
    combined.sort(key=lambda x: x.get('published_at', ''), reverse=True)
    
    save_articles(combined)
    return combined

if __name__ == "__main__":
    run_aggregation()
