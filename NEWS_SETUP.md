# Auto EV news – one-time setup

1. Put these in the root of your GitHub repo (same place as index.html):
   - index.html
   - news.json
   - scripts/update_news.py
   - .github/workflows/update-news.yml
2. In GitHub: Settings → Actions → General → Workflow permissions → "Read and write permissions" → Save.
3. Open the Actions tab → "Update EV news" → Run workflow (first run). After this it runs every 3 hours by itself.
4. Check that news.json now has headlines. Your hosting (Netlify / Vercel / Cloudflare Pages) redeploys automatically on each commit.

Change topics: edit INDIA_QUERIES, GLOBAL_QUERIES, MUST_HAVE and BLOCK at the top of scripts/update_news.py.
Note: the news panel will show "No headlines yet" if you open index.html straight from your computer, because browsers block loading news.json from a file. Use your live site or a local server.
