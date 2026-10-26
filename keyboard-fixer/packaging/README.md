# Package-manager distribution (winget, Scoop, Chocolatey)

`generate.py` builds manifests for a published release (hashes are read from the release's `SHA256SUMS.txt`):

```bash
python3 generate.py keyflip-v0.1.0-15 diamondrubinny/diamondrubinny   # writes packaging/generated/
```
Re-run it for every new release (tags look like `keyflip-v<major.minor.patch>-<build>`; the package version becomes `<major.minor.patch>.<build>`).
After the dedicated repo `diamondrubinny/keyflip` exists, pass it as the second argument.

## Status and what was verified (2026-10-26)
| Catalog | Needs approval? | What is confirmed | What is NOT confirmed (verify before relying) |
|---|---|---|---|
| **Scoop, own bucket** | No | A bucket is just a Git repo with `bucket/*.json` | Exact manifest options for your Scoop version |
| **Scoop Main / Extras** | Yes | Main requires a notable, widely used non-GUI tool (about 500 stars / 150 forks) and a stable release ([criteria](https://github.com/ScoopInstaller/Scoop/wiki/Criteria-for-including-apps-in-the-main-bucket)). KeyFlip is a GUI app and a pre-release, so Main is out | Extras criteria: read [CONTRIBUTING](https://github.com/ScoopInstaller/.github/blob/main/.github/CONTRIBUTING.md) |
| **winget** (`microsoft/winget-pkgs`) | Yes (automated validation, maybe manual review) | The [README](https://github.com/microsoft/winget-pkgs) says installers must be MSIX, MSI, APPX, MSIXBundle, APPXBundle or .exe application installers; submissions go through pull requests | Whether a **portable** .exe is accepted (the manifest schema has `InstallerType: portable`, see the [manifest docs](https://learn.microsoft.com/windows/package-manager/package/manifest)); how unsigned binaries are treated; the dependency id `Microsoft.DotNet.DesktopRuntime.8` |
| **Chocolatey community repo** | Yes (automated checks incl. VirusTotal, plus human review of every version) | Per the [moderation docs](https://docs.chocolatey.org/en-us/community-repository/moderation/) | Whether unsigned executables or keyboard-hook detections cause rejection |

None of these catalogs is proven to count as "reputation" for SignPath; they mainly make installation easier and increase visibility.

## Scoop (own bucket, no approval)
1. Create an empty public repo `scoop-keyflip` and push the ready-made content of `generated/scoop` (it already contains `bucket/keyflip.json` and a README):
```bash
git clone https://github.com/diamondrubinny/diamondrubinny.git && cd diamondrubinny && git checkout claude/typing-error-translation-addon-ae6d7h
git subtree split --prefix=keyboard-fixer/packaging/generated/scoop -b scoop-bucket
git push https://github.com/diamondrubinny/scoop-keyflip.git scoop-bucket:main
```
2. Users install with:
```powershell
scoop bucket add keyflip https://github.com/diamondrubinny/scoop-keyflip
scoop install keyflip
```

## winget
```powershell
winget settings --enable LocalManifestFiles        # administrator shell, once
winget validate --manifest generated\winget\d\diamondrubinny\KeyFlip\0.1.0.15
winget install  --manifest generated\winget\d\diamondrubinny\KeyFlip\0.1.0.15
```
If both pass, submit with [wingetcreate](https://github.com/microsoft/winget-create) (`wingetcreate submit`) or a pull request to `microsoft/winget-pkgs` (read `doc/README.md` and `doc/FirstContribution.md` there). Expect automated validation and possibly manual review; Microsoft may refuse a package.

## Chocolatey
```powershell
cd generated\chocolatey\keyflip
choco pack
choco install keyflip -s . -y          # local test
choco apikey --key <your key from community.chocolatey.org> --source https://push.chocolatey.org/
choco push keyflip.0.1.0.15.nupkg --source https://push.chocolatey.org/
```
Requires a free account on community.chocolatey.org. Fix every moderation finding and re-upload the same version. Add a short `VERIFICATION.txt` only if you embed binaries in the package (this package downloads the release asset instead).
