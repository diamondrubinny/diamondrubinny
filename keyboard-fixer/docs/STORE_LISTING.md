# טיוטת כרטיס חנות (Chrome Web Store) – דורש אימות מול התיעוד הרשמי

**שם:** KeyFlip – תיקון הקלדה בשפה שגויה
**תיאור קצר:** מתקן אוטומטית טקסט שהוקלד במקלדת הלא נכונה (עברית ↔ אנגלית). הכול מקומי, בלי שליחת מידע.
**תיאור ארוך:** מקלידים `akuo` ומקבלים `שלום`. KeyFlip מזהה בסוף כל מילה אם הוקלדה בשפה הלא נכונה ומתקן אותה. Ctrl+Z מבטל. המרה ידנית: Alt+Shift+Z.

## הצדקת הרשאות (Single purpose: המרת טקסט בין פריסות מקלדת)
- סקריפט תוכן ב-http/https: נדרש כדי לקרוא את המילה האחרונה בשדה הכתיבה ולהחליפה. אין שליחת מידע.
- `storage`: הגדרות מקומיות. `contextMenus`: המרה ידנית. `activeTab`: השבתה לפי אתר.

## Privacy practices
- אין איסוף נתוני משתמש. אין מכירה/העברה לצד שלישי. אין שימוש בנתונים מחוץ למטרה היחידה.
- קישור למדיניות הפרטיות: `https://github.com/diamondrubinny/keyflip/blob/main/docs/PRIVACY.en.md` (יעבוד אחרי שהקוד יידחף לריפו `keyflip`; עד אז: `https://github.com/diamondrubinny/diamondrubinny/blob/claude/typing-error-translation-addon-ae6d7h/keyboard-fixer/docs/PRIVACY.en.md`).

## חומרים
- צילומי מסך מוכנים (1366×768) ב-`docs/screenshots/` (01–05). חסרים צילומי אפליקציית Windows: ראו `docs/screenshots/README.md`.
- אייקון 128 קיים ב-`extension/icons/128.png`. Chrome Web Store דורש חשבון מפתח ודמי רישום חד-פעמיים (לאמת); Microsoft Store: ראו `docs/MICROSOFT_STORE.md`.
