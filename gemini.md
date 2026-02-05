# Project Constitution

## Data Schemas

### Core Entity: Article
The primary unit of data flowing through the system.

```json
{
  "id": "string (UUID v4)",
  "title": "string",
  "url": "string (valid URL)",
  "source": "string (enum: 'BensBytes', 'AIRundown', 'Reddit', 'Other')",
  "published_at": "string (ISO 8601 datetime)",
  "summary": "string (markdown supported)",
  "content_snippet": "string (optional)",
  "tags": ["string"],
  "is_saved": "boolean (default: false)",
  "fetched_at": "string (ISO 8601 datetime)"
}
```

### Storage: Local State (Initial)
Structure for client-side persistence (before Supabase integration).

```json
{
  "last_fetch": "string (ISO 8601 datetime)",
  "articles": ["Article"],
  "saved_article_ids": ["string (UUID)"]
}
```

## Behavioral Rules
1.  **Visual Excellence**: Interface must be "gorgeous," "interactive," and "premium." Use animations, distinct cards, and modern typography.
2.  **Freshness**: Only display/consider data from the last 24 hours during the fetch cycle.
3.  **Persistence**: "Saved" articles must persist across refreshes. Unsaved articles can disappear if expired.
4.  **Scraping Etiquette**: Respect `robots.txt` where possible; use established libraries (BeautifulSoup/Playwright) deterministically.
5.  **Data Flow**: Scraper -> Parsing -> Deduplication -> UI Display -> User Action (Save/Read).

## Architectural Invariants
-   **Frontend**: Vite + React (TypeScript) for "Interactive Dashboard" capabilities.
-   **Styling**: TailwindCSS (Modern, flexible for "beautiful" designs) or Vanilla CSS with variables if preferred. *Decision: React + Tailwind for speed & interactive quality.*
-   **3-Layer Architecture**:
    1.  **Architecture**: SOPs in `architecture/`.
    2.  **Navigation**: Routing logic.
    3.  **Tools**: Atomic, deterministic Python scripts in `tools/` for scraping.
-   **Data-First Rule**: Defining `gemini.md` schema is mandatory before any `tools/` code.

## Maintenance Log
- **[Init]**: Project Memory initialized.
- **[Blueprint]**: Schema defined for `Article` entity.
