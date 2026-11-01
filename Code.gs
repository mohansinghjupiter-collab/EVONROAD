/**
 * EVonRoad leads -> Google Sheet
 * Paste this whole file into Extensions > Apps Script (see SHEETS_SETUP.md).
 */
const SHEET_NAME = 'Leads';
const NOTIFY_EMAIL = '';          // optional: your email to get an alert for each lead, e.g. 'you@gmail.com'
const HEADERS = ['Time (IST)', 'Type', 'Name', 'Phone', 'Email', 'City', 'PIN', 'Interested in', 'City on site', 'Page'];

function doPost(e) {
  try {
    const d = JSON.parse(e.postData.contents);

    // Server-side checks (never trust the browser)
    const email = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(String(d.email || '').trim()) ? clean(String(d.email).trim().toLowerCase(), 100) : '';
    const name = clean(d.name, 60), phone = String(d.phone || '').replace(/\D/g, ''),
          city = clean(d.city, 60), pin = String(d.pincode || '').replace(/\D/g, ''),
          interest = clean(d.interest, 120), type = d.type === 'Launch alert' ? 'Launch alert' : 'Test drive';
    if (name.length < 2 || !/^[6-9]\d{9}$/.test(phone) || city.length < 2 || !/^[1-9]\d{5}$/.test(pin)) {
      return out({ ok: false, error: 'invalid' });
    }

    const lock = LockService.getScriptLock();
    lock.waitLock(20000);
    try {
      const ss = SpreadsheetApp.getActiveSpreadsheet();
      let sh = ss.getSheetByName(SHEET_NAME);
      if (!sh) {
        sh = ss.insertSheet(SHEET_NAME);
        sh.appendRow(HEADERS);
        sh.setFrozenRows(1);
      }

      // Ignore the same phone + same interest within 24 hours
      const last = sh.getLastRow();
      if (last > 1) {
        const rows = sh.getRange(Math.max(2, last - 199), 1, Math.min(200, last - 1), 8).getValues();
        const dayAgo = Date.now() - 24 * 3600 * 1000;
        for (const r of rows) {
          if (String(r[3]).replace(/\D/g, '') === phone && String(r[7]) === interest) {
            const t = new Date(r[0]).getTime();
            if (!isNaN(t) && t > dayAgo) return out({ ok: true, duplicate: true });
          }
        }
      }

      const when = Utilities.formatDate(new Date(), 'Asia/Kolkata', 'yyyy-MM-dd HH:mm:ss');
      sh.appendRow([when, type, name, "'" + phone, email, city, "'" + pin, interest, clean(d.siteCity, 40), clean(d.page, 200)]);
    } finally {
      lock.releaseLock();
    }

    if (NOTIFY_EMAIL) {
      MailApp.sendEmail(NOTIFY_EMAIL, 'New EVonRoad lead: ' + type,
        name + '\n' + phone + (email ? '\n' + email : '') + '\n' + city + ' - ' + pin + '\n' + interest);
    }
    return out({ ok: true });
  } catch (err) {
    return out({ ok: false, error: String(err) });
  }
}

// Stops spreadsheet formulas from being injected (=, +, -, @ at the start)
function clean(v, max) {
  let s = String(v == null ? '' : v).replace(/[\r\n\t]+/g, ' ').trim().slice(0, max);
  if (/^[=+\-@]/.test(s)) s = "'" + s;
  return s;
}
function out(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
