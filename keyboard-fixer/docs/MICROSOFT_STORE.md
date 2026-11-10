# Publishing KeyFlip on the Microsoft Store

The Store signs MSIX packages itself, so **no code-signing certificate is needed** and Windows shows no SmartScreen warning for Store installs.
Registration for individual developers is free according to [Microsoft's announcement](https://blogs.windows.com/windowsdeveloper/2025/09/10/free-developer-registration-for-individual-developers-on-microsoft-store/)
(Microsoft account, ID and selfie verification; verify the current terms on the sign-up page). Everything below is a checklist; the registration, identity verification and submission must be done by the account owner.

## What is already prepared
- `desktop/msix/AppxManifest.template.xml` and `desktop/msix/Assets/` (logos), packaged by the CI job *Build MSIX package*.
- The CI artifact `keyflip-msix-store-package` (`KeyFlip.msix`, unsigned, self-contained build). It is built with placeholder identity values until you set the repository variables below.
- The Windows app detects the Store build and hides the registry-based "Start with Windows" menu item (the package has a startup task instead: Settings > Apps > Startup).
- Listing text: `docs/STORE_LISTING.md`; privacy policy: `docs/PRIVACY.en.md`.

## Steps
1. Create the developer account: https://storedeveloper.microsoft.com (individual account, free).
2. In Partner Center: **Apps and games > New product > MSIX or PWA app**, reserve the name **KeyFlip**.
3. Open **Product management > Product identity** and copy three values:
   - `Package/Identity/Name`  -> repository variable `MSIX_IDENTITY_NAME`
   - `Package/Identity/Publisher` (looks like `CN=xxxxxxxx-xxxx-...`) -> `MSIX_PUBLISHER`
   - `Package/Properties/PublisherDisplayName` -> `MSIX_PUBLISHER_DISPLAY`
   Add them in GitHub: repository **Settings > Secrets and variables > Actions > Variables**.
4. Run the workflow (Actions > KeyFlip > Run workflow), download the artifact `keyflip-msix-store-package`, unzip it to get `KeyFlip.msix`.
5. In the submission: upload `KeyFlip.msix`; category *Productivity* (or *Utilities & tools*); fill the listing from `docs/STORE_LISTING.md`;
   add a **privacy policy URL** (the public URL of `docs/PRIVACY.en.md` in the final repo); add screenshots (1366x768 or larger, at least one).
6. **Restricted capability `runFullTrust`:** Partner Center asks why it is needed. Suggested text:
   > KeyFlip is a Win32 desktop app packaged as MSIX. It needs full trust to register a global hotkey, observe key presses to detect the end of a typed word, and send corrected text to the active application. All processing is local: no network access, nothing is logged or stored.
7. **Notes for certification** (the keyboard hook is the most likely review topic; the Store policies for it were not checked while preparing this document, so read the current [Store policies](https://learn.microsoft.com/windows/apps/publish/store-policies) first):
   > The app corrects text typed in the wrong keyboard layout (Hebrew/English). It uses a low-level keyboard hook only to detect word boundaries, keeps at most the current line (200 characters) in memory, writes nothing to disk and makes no network calls. It skips password fields, password managers, terminals and browsers by default. Source code: <repository URL>. To test: start the app, switch the keyboard to English and type "akuo " in Notepad; it becomes "שלום ".
8. Age rating questionnaire: no user-generated content, no online features.

## Known risks
- Store review may question the keyboard hook or the full-trust capability; be ready to answer with the notes above or to remove the feature.
- A self-contained build makes the package large (about 150 MB); that is allowed but slows downloads.
- Updates: upload a new MSIX to the same submission with a higher version (the CI version is `0.1.<build>.0`).
- Not yet tested on Windows: install the package locally first (sideloading needs developer mode because it is unsigned) or use the Windows App Certification Kit.
