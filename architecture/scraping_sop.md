# Scraping Standard Operating Procedure (SOP)

## 1. Goal
Extract article metadata (Title, URL, Date, Summary) from target sources deterministically and respectfully.

## 2. Tools & Libraries
-   **Language**: Python 3.x
-   **Libraries**:
    -   `requests`: For fetching HTML.
    -   `beautifulsoup4`: For parsing HTML.
    -   `praw` (optional): For Reddit API if needed (fallback to `.json`).
    -   `datetime`: For normalizing dates.

## 3. Target Specifications

### Source A: Ben's Bites
-   **URL**: `https://bensbites.substack.com/archive`
-   **Method**: `requests.get` -> `BeautifulSoup`
-   **Selectors**:
    -   **Container**: `div.portable-archive-post` (or similar, widely used in Substack).
    -   **Title**: `a.post-preview-title` (text).
    -   **URL**: `a.post-preview-title` via `href`.
    -   **Date**: `time` element or text date in `div.post-preview-meta`.
-   **Rate Limit**: 1 request per hour (polite).

### Source B: The AI Rundown
-   **URL**: `https://www.therundown.ai/`
-   **Method**: `requests.get` -> `BeautifulSoup`
-   **Selectors**:
    -   **Container**: Look for `div` containing `h3` headers under "Latest Articles".
    -   **Title**: `h3` text.
    -   **URL**: `a` tag wrapping the `h3` or adjacent.
-   **Rate Limit**: 1 request per hour.

### Source C: Reddit (r/ArtificialInteligence)
-   **Method**: JSON Endpoint.
-   **URL**: `https://www.reddit.com/r/ArtificialInteligence/new.json?limit=10`
-   **Headers**: Must include `User-Agent: scripts/1.0 (by /u/yourname)`.
-   **Parsing**: `data['data']['children'][i]['data']['title']`, `['url']`, `['created_utc']`.

## 4. Output Schema (Normalized)
Each scraper function returns a list of dictionaries matching the `gemini.md` schema:
```python
{
    "id": str(uuid.uuid4()),
    "title": str,
    "url": str,
    "source": "BensBites" | "TheRundown" | "Reddit",
    "published_at": str(iso8601),
    "summary": str(optional),
    "tags": [],
    "is_saved": False
}
```

## 5. Error Handling
-   **Network**: Retry 3 times with exponential backoff.
-   **Parsing**: If selectors fail, log error to `scraping_errors.log` and skip item (do not crash).
-   **Validation**: Discard items without Title or URL.
