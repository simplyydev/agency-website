# Security Audit Report

## 1. Secrets & Credentials
- [x] **API Keys**: No hardcoded API keys found in codebase. Reddit scraper uses public JSON endpoint.
- [x] **Env Vars**: Project is configured to load from `.env`, but no `.env` file is currently committed (good practice).
- [x] **Git**: `.gitignore` is correctly configured to exclude `.env`, `node_modules`, and `data/` (user data).

## 2. Dependencies
- **Python**: `requests`, `beautifulsoup4`. Standard libraries, no known critical vulnerabilities in latest versions.
- **Node**: `vite`, `react`, `tailwindcss`. Standard stack. `npm audit` should be run periodically.

## 3. Data Privacy
- **Scraping**: Scripts respect public endpoints (`/archive`, `.json`). No abusive rate limits hardcoded (scripts run once).
- **Storage**: Data is stored locally in `data/articles.json` and client-side `localStorage`. No PII is collected.

## 4. Code Quality
- **Type Safety**: Frontend uses TypeScript definitions for `Article` schema.
- **Error Handling**: Scrapers have `try/except` blocks to prevent crashes on network failures.

## 5. Recommendation
- **Next Step**: When moving to production (Supabase), ensure `SUPABASE_KEY` is added to `.env` and never committed.
