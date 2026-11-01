# EVonRoad on GitHub + Cloudflare (easy updates, no re-uploading the whole site)

Do Part A once. After that, Part B is all you ever do.

## Part A: one-time setup (about 15 minutes)

### 1. Make a GitHub repository
1. Go to github.com, sign in (or sign up, it is free).
2. Click **+** (top right) > **New repository**.
3. Name: `evonroad`. Choose **Public**. Click **Create repository**.

### 2. Put the website in it
1. On the new empty repo page, click **uploading an existing file**.
2. Unzip `evonroad-site.zip` on your computer. Open the unzipped folder.
3. Select everything inside it EXCEPT the `.github` folder, and drag it all into the GitHub page. (You can see `index.html`, `images`, `scripts`, `news.json` and so on.)
4. Click **Commit changes**.

### 3. Add the news robot file (by typing, because dot-folders do not upload well)
1. Click **Add file** > **Create new file**.
2. In the name box type exactly: `.github/workflows/update-news.yml`
   (typing the slashes makes the folders for you)
3. Open `update-news.yml` from your unzipped folder, copy everything, paste it into the big box.
4. Click **Commit changes**.
5. Go to **Settings** > **Actions** > **General** > **Workflow permissions** > choose **Read and write permissions** > **Save**.
6. Go to the **Actions** tab, click **Update EV news**, then **Run workflow**. A green tick means the news works. After this it runs by itself every 3 hours.

### 4. Connect it to Cloudflare Pages
Your earlier Cloudflare project was made by upload. Cloudflare cannot turn that into a GitHub project, so make a new one:
1. dash.cloudflare.com > **Workers & Pages** > **Create** > **Pages** > **Connect to Git**.
2. Allow GitHub, choose the `evonroad` repo, click **Begin setup**.
3. Framework preset: **None**. Build command: leave empty. Build output directory: leave empty (or type `/`). Click **Save and Deploy**.
4. Open the project > **Custom domains** and add your domain. Then remove the old upload project.

From now on, every change you save in GitHub goes live in about a minute.

## Part B: adding photos and logos (the normal routine)

1. Open your live site with `?admin=true` on the end. Log in.
2. Upload about 15 photos / logos.
3. Tap **Photos ZIP** in the amber bar. A ZIP downloads. Unzip it.
4. In GitHub, open your `evonroad` repo > **Add file** > **Upload files**.
5. Drag in the `images` folder and `photos.json` from the unzipped ZIP. When asked, replacing `photos.json` is fine.
6. Click **Commit changes**. Wait about a minute for Cloudflare to publish.
7. Reload your site admin page, then tap **Reset** in the admin bar to free browser space. Repeat from step 2 with the next batch.

Rules that avoid problems
- Wait for the site to publish and reload the admin page BEFORE pressing Reset. The page needs the new `photos.json` to remember earlier photos.
- Never upload `news.json` yourself. The news robot owns it.
- Upload new files into the same repo each time. Nothing is lost, GitHub keeps every version, so you can undo any mistake.

## Changing text or prices
Open `index.html` in GitHub, click the pencil icon, edit, click **Commit changes**. (It is a big file, so for large edits ask me to give you the updated file and upload it with **Add file** > **Upload files**.)

## Discontinued vehicles (new)
When a manufacturer stops selling a trim:
1. Open your site with `?admin=true` and log in.
2. Tap **🚫 Discontinued** in the amber bar. Search for the vehicle, tick the trim (or tap **Discontinue all** for the whole model). You can also tap **🚫 Discontinue** on any card.
3. Tap **📦 Photos ZIP**, unzip, and upload `photos.json` to GitHub (same as for photos). The status goes live in about a minute.

What visitors see: discontinued trims disappear from the main list, Compare and the price calculator. A **Show discontinued** button above the list lets people still look them up, with a red "DISCONTINUED" label and no price.
Changed your mind? Tick the trim off (or tap **Restore**) and export again.
Tip: always export from an admin page that has loaded your live site, so earlier photos and statuses are carried along.
