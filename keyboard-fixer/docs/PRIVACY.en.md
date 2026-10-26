# KeyFlip Privacy Policy

Last updated: 2026-10-26 · Policy version 0.1 · Contact: d@rubinny.net

> Technical draft; have it reviewed legally before wider distribution. (Hebrew version: [PRIVACY.md](PRIVACY.md))

## Summary
KeyFlip (Chrome extension and Windows tray app) fixes text typed in the wrong keyboard layout between Hebrew and English.
**All processing happens on your device. KeyFlip does not send text, keystrokes or usage data to any server. It contains no analytics, advertising, tracking pixels or cookies, and makes no network requests.**

## What data is processed

| Data | Purpose | Where it lives | Retention | Third parties |
|---|---|---|---|---|
| Text typed in editable fields (extension) | Detect and convert a word typed in the wrong layout | Browser memory only | Moments (one word) | None |
| The current line typed (Windows app) | Same, plus manual conversion | App memory only, max. 200 characters | Cleared on Enter/Tab/mouse click/window change/30 s idle/exit | None |
| Clipboard text (Windows app, manual conversion of selected text) | Read the selected text | Memory; the previous clipboard text is restored immediately | Under one second | None |
| Settings (on/off, disabled sites, ignored apps) | Configure behavior | `chrome.storage.local`, or `%APPDATA%\KeyFlip\settings.json` | Until you uninstall | None |

KeyFlip never writes typed text to disk or to logs.

## The keyboard hook (Windows app)
The Windows app uses a low-level keyboard hook only to detect when a word has ended. It does not record, store, log or transmit keystrokes beyond the in-memory line described above.
It does not act in password managers, terminals, remote-control tools, classic Windows password fields, or (by default) web browsers, where the Chrome extension is used instead. If you enable "Also work in browsers", password fields inside web pages cannot be detected, so disable it when typing passwords.

## Chrome extension permissions
- Content script on http/https pages: reads the last typed word in an editable field and replaces it. Password, payment-card and one-time-code fields and code editors are skipped.
- `storage`: local settings. `contextMenus`: the "convert selection" menu item. `activeTab`: lets the popup show and toggle the current site.

## Your rights
Because KeyFlip collects no personal data, there is nothing to access, correct or delete on our side. To remove everything, uninstall the extension/app and delete `%APPDATA%\KeyFlip`.

## Children
KeyFlip collects no information from anyone, including children.

## Changes
Changes will be published here with a new version number.
