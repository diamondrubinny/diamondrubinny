# KeyFlip

> Fixes text typed in the wrong keyboard layout between Hebrew and English, locally and without sending any data.
> Chrome extension and Windows tray app.

Typed `akuo` instead of `שלום`, or `יקךךם` instead of `hello`? KeyFlip detects the wrong layout at the end of each word and fixes it for you.

[![CI](../../actions/workflows/ci.yml/badge.svg)](../../actions/workflows/ci.yml) ![License](https://img.shields.io/badge/license-Apache--2.0-blue)

- **[Code signing policy](docs/CODE_SIGNING_POLICY.md)** · [Privacy policy](docs/PRIVACY.en.md) · [Accessibility statement (draft)](docs/ACCESSIBILITY.md)
- **Download:** see the [Releases](../../releases) page (Windows `KeyFlip.exe`, Chrome extension ZIP, SHA256 checksums).
- Hebrew documentation: [below](#מתקן-טקסט-שהוקלד-בטעות-במקלדת-הלא-נכונה).

## Features
- **Automatic correction:** type a word and press space; if it looks like it was typed in the wrong layout it is replaced. `Ctrl+Z` undoes it (extension); `Ctrl+Alt+Space` right after a fix undoes it (Windows app).
- **Manual conversion:** select text (or leave the caret after the words) and press `Alt+Shift+Z` (extension) or `Ctrl+Alt+Space` (Windows app).
- **Offline and private:** dictionary-based detection runs entirely on your device. No network requests, no analytics, no cookies.
- **Safe by default:** never touches password fields (the extension also skips fields named or labelled like passwords/PIN/OTP/card numbers and CSS-masked inputs; the Windows app asks Windows UI Automation whether the focused control is a password field and does nothing if it cannot tell), skips payment-card and one-time-code fields, code editors, words containing digits, `@`, URLs or capital letters; the Windows app also skips password managers, terminals and (by default) browsers.
- **Accessible UI:** RTL Hebrew, keyboard operable, light/dark themes, automated WCAG 2.1 A/AA scan (axe-core).

## Install
**Windows app:** download `KeyFlip-windows-x64-self-contained.exe` from [Releases](../../releases) and run it (tray icon). The build is unsigned until the SignPath Foundation application is approved, so SmartScreen may warn: choose *More info → Run anyway*, or right-click the file → *Properties → Unblock*. Verify the file with `SHA256SUMS.txt`.

**Chrome extension:** download and unzip `KeyFlip-chrome-extension.zip`, open `chrome://extensions`, enable *Developer mode*, choose *Load unpacked* and select the folder.

Use either the extension or the app's "Also work in browsers" toggle, not both, to avoid double correction. In browsers the extension is recommended because it detects password fields most reliably.

## Build and test
```bash
# Chrome extension
cd extension && npm install
npm test && npm run typecheck && npm run build   # output in extension/dist
npm run e2e      # real Chromium end-to-end tests (needs Playwright)
npm run a11y     # axe-core accessibility scan
npm run eval     # detection accuracy on held-out words

# Windows app (Windows, .NET 8 SDK)
dotnet test desktop/KeyFlip.Core.Tests
dotnet publish desktop/KeyFlip.App -c Release -r win-x64
```
The layout mapping (`shared/mapping.json`) and test cases (`shared/test-cases.json`) are shared by both implementations.

## How accurate is it?
Measured on words the detector had never seen: about **91%** of wrongly typed Hebrew and **88%** of wrongly typed English words (5+ letters) are recovered, and roughly **0.8%** of rare valid words are corrected by mistake. Short words are the hard part. Details and method: [docs/ACCURACY.md](docs/ACCURACY.md).

## Privacy and transparency
- The code makes no network requests. Typed text is processed in memory only and never written to disk or logs.
- The Windows app uses a low-level keyboard hook only to detect the end of a word and keeps at most the current line (200 characters) in memory.
- All binaries are built by GitHub Actions from this public source. Third-party data: see [NOTICE.md](NOTICE.md).
- Status: early-stage open-source project; it does not yet have broad adoption.

## Known limitations
- Google Docs and other canvas-based editors may not support text replacement.
- Windows apps running as administrator cannot receive input from a non-elevated app.
- Detection is statistical and not perfect (a lone two-letter word is never changed); the manual shortcut is always available.

## License
[Apache-2.0](LICENSE). Word lists are derived from FrequencyWords (CC BY-SA); see [NOTICE.md](NOTICE.md).

---

מתקן טקסט שהוקלד בטעות במקלדת הלא נכונה: `akuo` ← `שלום`, `יקךךם` ← `hello`.

- `extension/` – תוסף Chrome (Manifest V3).
- `desktop/` – תוכנת Windows (Tray, .NET 8). נבנית ונבדקת ב-GitHub Actions (`.github/workflows/ci.yml`).
- `shared/` – מיפוי המקלדת המשותף (`mapping.json`) ומקרי בדיקה.

## תוסף Chrome

```bash
cd extension
npm install
npm test          # בדיקות יחידה
npm run typecheck
npm run build     # יוצר extension/dist
npm run e2e       # בדיקה בדפדפן אמיתי (דורש build ו-Playwright)
npm run eval      # מדידת דיוק הזיהוי
npm run a11y      # בדיקת נגישות אוטומטית (axe-core)
```

התקנה: `chrome://extensions` ← מצב מפתח ← "טען תוסף לא ארוז" ← בחרו את `extension/dist`.

### שימוש
- **אוטומטי:** מקלידים מילה ולוחצים רווח. אם המילה נראית כאילו הוקלדה בשפה שגויה היא מוחלפת. `Ctrl+Z` מבטל.
- **ידני:** מסמנים טקסט (או משאירים את הסמן אחרי המילים) ו-`Alt+Shift+Z`, או תפריט הקשר.
- **הגדרות:** בחלון התוסף (השבתה לפי אתר) ובדף האפשרויות.

### פרטיות ואבטחה
- אין רשת: שום טקסט לא יוצא מהמחשב. אין אנליטיקה ואין עוגיות.
- הרשאות: `storage` (הגדרות), `contextMenus`, `activeTab` (חלון התוסף). סקריפט התוכן רץ בדפי http/https כדי לזהות הקלדה.
- לא פועל בשדות סיסמה, כרטיס אשראי, קוד חד-פעמי, עורכי קוד, ובמילים עם ספרות, `@`, כתובות או אותיות גדולות.

### מגבלות
- Google Docs ועורכי canvas אחרים עלולים לא לתמוך.
- הזיהוי מבוסס מילונים ומודל סטטיסטי: כ-91% שחזור של מילים שלא היו במילון ובאורך 5+ אותיות, וכ-0.8% תיקון שגוי של מילים נדירות. מילה קצרה בודדת לא משתנה. פירוט ושיטת המדידה: `docs/ACCURACY.md`.

> מסמכי מדיניות פרטיות והצהרת נגישות הם טיוטות הדורשות בדיקה מקצועית לפני פרסום.

## תוכנת Windows

- **אוטומטי:** אחרי כל מילה (רווח) נבדקת המילה ומתוקנת אם הוקלדה בשפה שגויה. `Ctrl+Alt+Space` מיד אחרי תיקון מבטל אותו.
- **ידני:** `Ctrl+Alt+Space` ממיר את הטקסט המסומן, או את המילים האחרונות שהוקלדו בשורה.
- **פרטיות:** משתמשת ב-keyboard hook כדי לזהות סוף מילה. שומרת בזיכרון רק את השורה הנוכחית (עד 200 תווים), ללא דיסק/לוג/רשת. כברירת מחדל לא פועלת בדפדפנים (התוסף מטפל בהם), מנהלי סיסמאות, טרמינלים ושדות סיסמה קלאסיים. רשימת התוכנות המוחרגות: `%APPDATA%\KeyFlip\settings.json`.
- **דפדפנים:** אפשר להפעיל מתפריט המגש "פעל גם בדפדפנים" (שימושי בלי התוסף, או לשורת הכתובת). אל תפעילו יחד עם התוסף כדי למנוע תיקון כפול. בדפדפן אין זיהוי שדות סיסמה.
- **בנייה מקומית (Windows):** `dotnet test desktop/KeyFlip.Core.Tests` ואז `dotnet publish desktop/KeyFlip.App -c Release -r win-x64`.
- **מגבלות:** לא פועלת בחלונות שרצים כמנהל; תוכנות שחוסמות הקלדה מדומה יפעלו חלקית; ההמרה הידנית של טקסט מסומן משתמשת בלוח (ומשחזרת טקסט בלבד); אנטי-וירוס עלול לסמן תוכנה עם keyboard hook (False Positive), לכן מומלץ חתימה דיגיטלית לפני הפצה.

## מסמכים (טיוטות לבדיקה משפטית/מקצועית)
`docs/PRIVACY.md`, `docs/TERMS.md`, `docs/ACCESSIBILITY.md`, `docs/STORE_LISTING.md`, `docs/PRODUCTION_CHECKLIST.md`.

## רישיון
Apache-2.0. מילוני הזיהוי נגזרים מנתונים ברישיון CC BY-SA (ראו `NOTICE.md`).
