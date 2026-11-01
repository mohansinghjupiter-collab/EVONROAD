# Deploy EVonRoad (pick ONE way)

This folder is the whole website. No build step is needed.

## A. Cloudflare Pages (recommended, free)
1. Create a free account at dash.cloudflare.com, then Workers & Pages > Create > Pages > **Upload assets**.
2. Name the project `evonroad`, upload this folder (or the zip), click **Deploy**.
3. You get a link like `evonroad.pages.dev` straight away.
4. Add your domain: project > Custom domains > Set up a custom domain > `evonroad.in`.

## B. Netlify (also free)
1. Go to app.netlify.com/drop and drag this folder onto the page.
2. You get a link like `something.netlify.app` in seconds.
3. Domain: Site configuration > Domain management > Add a domain.

## C. GitHub + automatic news (best for the long run) - see GITHUB_SETUP.md for the full steps
1. Upload everything in this folder to a new GitHub repo (see NEWS_SETUP.md).
2. Connect that repo to Cloudflare Pages or Netlify ("Connect to Git"). Every time the news bot saves news.json, the site updates itself.

## After it is live
- Test on your phone and a PC.
- Add photos to `images/` and logos to `images/brands/` any time. Re-upload the folder (or push to GitHub).
- Fill in `LEADS_ENDPOINT` in index.html (see SHEETS_SETUP.md) to turn on the test drive and notify buttons.
- If your domain is not evonroad.in, replace `https://evonroad.in` in index.html, robots.txt and sitemap.xml.
