# Receive leads in Google Sheets (about 10 minutes, free)

1. Go to sheets.google.com and create a new blank spreadsheet. Name it "EVonRoad Leads".
2. Click **Extensions > Apps Script**.
3. Delete everything in the editor, then paste the full contents of `Code.gs`. Optional: put your email in `NOTIFY_EMAIL` to get an email for each lead.
4. Click **Save**, then **Deploy > New deployment**.
   - Click the gear icon, choose **Web app**.
   - Execute as: **Me**.
   - Who has access: **Anyone**.
   - Click **Deploy** and allow the permissions. (If Google says "app not verified", click Advanced > Go to project. This is your own script.)
5. Copy the **Web app URL** (starts with https://script.google.com/macros/s/...).
6. Open `index.html`, search for `const LEADS_ENDPOINT = "";` and paste the URL between the quotes. Just below it, also fill in `CONTACT_EMAIL` (your site contact email, also used in the Privacy Policy and About Us). The form buttons stay hidden until both are filled.
7. Upload the new `index.html`. The Book Test Drive and Notify buttons appear.
8. Test it: submit the form with your own number. A new row should appear in the "Leads" tab within seconds.

Notes
- The form has an optional Email field. In the sheet it appears as the "Email" column (empty if the visitor skipped it). If you already created the sheet with an older version of Code.gs, delete the "Leads" tab so it is rebuilt with the new columns.
- If you change Code.gs later, use **Deploy > Manage deployments > Edit > New version**. The URL stays the same.
- Keep the sheet private. Share it only with people who need the leads.
- The privacy policy opens from the footer and from the form's consent tick box. Check the wording, especially the retention period (`LEAD_RETENTION`), and have a lawyer review it before launch.
