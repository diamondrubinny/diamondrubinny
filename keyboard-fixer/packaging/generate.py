#!/usr/bin/env python3
"""Generates winget, Scoop and Chocolatey package files for a KeyFlip GitHub release.
Usage: python3 generate.py <release-tag> [owner/repo]
Example: python3 generate.py keyflip-v0.1.0-15 diamondrubinny/diamondrubinny
Reads SHA256SUMS.txt from the release, so hashes always match the published files. Output: packaging/generated/."""
import re, sys, urllib.request, pathlib, textwrap

tag = sys.argv[1]
repo = sys.argv[2] if len(sys.argv) > 2 else 'diamondrubinny/diamondrubinny'
owner = repo.split('/')[0]
m = re.fullmatch(r'keyflip-v(\d+\.\d+\.\d+)-(\d+)', tag)
if not m:
    sys.exit('tag must look like keyflip-v0.1.0-15')
version = f'{m.group(1)}.{m.group(2)}'          # 0.1.0.15 (four-part, valid for winget/Scoop/NuGet)
base = f'https://github.com/{repo}/releases/download/{tag}'
sums = urllib.request.urlopen(f'{base}/SHA256SUMS.txt').read().decode()
hashes = {name.strip().lstrip('*'): h for h, name in (l.split(None, 1) for l in sums.splitlines() if l.strip())}
SC = 'KeyFlip-windows-x64-self-contained.exe'
FD = 'KeyFlip-windows-x64-needs-dotnet8.exe'
for need in (SC, FD):
    if need not in hashes:
        sys.exit(f'{need} not found in SHA256SUMS.txt')

out = pathlib.Path(__file__).parent / 'generated'
desc = 'Fixes text typed in the wrong keyboard layout between Hebrew and English.'
long_desc = ('KeyFlip fixes Hebrew/English typing mistakes made in the wrong keyboard layout, '
             'automatically at the end of each word or on demand with Ctrl+Alt+Space. It runs locally, sends no data, '
             'and never touches password fields.')

# ---- winget (3 files, manifest schema 1.6.0; verify with `winget validate`)
wg = out / 'winget' / f'{owner[0].lower()}' / owner / 'KeyFlip' / version
wg.mkdir(parents=True, exist_ok=True)
pid = f'{owner}.KeyFlip'
(wg / f'{pid}.yaml').write_text(textwrap.dedent(f'''\
    # yaml-language-server: $schema=https://aka.ms/winget-manifest.version.1.6.0.schema.json
    PackageIdentifier: {pid}
    PackageVersion: {version}
    DefaultLocale: en-US
    ManifestType: version
    ManifestVersion: 1.6.0
    '''))
(wg / f'{pid}.installer.yaml').write_text(textwrap.dedent(f'''\
    # yaml-language-server: $schema=https://aka.ms/winget-manifest.installer.1.6.0.schema.json
    PackageIdentifier: {pid}
    PackageVersion: {version}
    InstallerType: portable
    Commands:
    - keyflip
    Dependencies:
      PackageDependencies:
      - PackageIdentifier: Microsoft.DotNet.DesktopRuntime.8
    Installers:
    - Architecture: x64
      InstallerUrl: {base}/{FD}
      InstallerSha256: {hashes[FD].upper()}
    ManifestType: installer
    ManifestVersion: 1.6.0
    '''))
(wg / f'{pid}.locale.en-US.yaml').write_text(textwrap.dedent(f'''\
    # yaml-language-server: $schema=https://aka.ms/winget-manifest.defaultLocale.1.6.0.schema.json
    PackageIdentifier: {pid}
    PackageVersion: {version}
    PackageLocale: en-US
    Publisher: {owner}
    PublisherUrl: https://github.com/{owner}
    PackageName: KeyFlip
    PackageUrl: https://github.com/{repo}
    License: Apache-2.0
    LicenseUrl: https://github.com/{repo}/blob/HEAD/LICENSE
    ShortDescription: {desc}
    Description: {long_desc}
    Moniker: keyflip
    Tags:
    - hebrew
    - keyboard
    - layout
    - typing
    - productivity
    ManifestType: defaultLocale
    ManifestVersion: 1.6.0
    '''))

# ---- Scoop (own bucket: bucket/keyflip.json). Uses the self-contained build, so no runtime dependency.
sc = out / 'scoop' / 'bucket'
sc.mkdir(parents=True, exist_ok=True)
(sc / 'keyflip.json').write_text(textwrap.dedent(f'''\
    {{
        "version": "{version}",
        "description": "{desc}",
        "homepage": "https://github.com/{repo}",
        "license": "Apache-2.0",
        "url": "{base}/{SC}#/KeyFlip.exe",
        "hash": "{hashes[SC]}",
        "bin": "KeyFlip.exe",
        "shortcuts": [
            ["KeyFlip.exe", "KeyFlip"]
        ]
    }}
    '''))

# ---- Chocolatey (self-contained build downloaded at install time)
ch = out / 'chocolatey' / 'keyflip'
(ch / 'tools').mkdir(parents=True, exist_ok=True)
(ch / 'keyflip.nuspec').write_text(textwrap.dedent(f'''\
    <?xml version="1.0" encoding="utf-8"?>
    <package xmlns="http://schemas.microsoft.com/packaging/2015/06/nuspec.xsd">
      <metadata>
        <id>keyflip</id>
        <version>{version}</version>
        <title>KeyFlip</title>
        <authors>{owner}</authors>
        <projectUrl>https://github.com/{repo}</projectUrl>
        <packageSourceUrl>https://github.com/{repo}/tree/HEAD/keyboard-fixer/packaging</packageSourceUrl>
        <licenseUrl>https://github.com/{repo}/blob/HEAD/LICENSE</licenseUrl>
        <requireLicenseAcceptance>false</requireLicenseAcceptance>
        <projectSourceUrl>https://github.com/{repo}</projectSourceUrl>
        <bugTrackerUrl>https://github.com/{repo}/issues</bugTrackerUrl>
        <tags>hebrew keyboard layout typing productivity</tags>
        <summary>{desc}</summary>
        <description>{long_desc}</description>
      </metadata>
      <files>
        <file src="tools\\**" target="tools" />
      </files>
    </package>
    '''))
(ch / 'tools' / 'chocolateyinstall.ps1').write_text(textwrap.dedent(f'''\
    $ErrorActionPreference = 'Stop'
    $toolsDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
    Get-ChocolateyWebFile -PackageName 'keyflip' `
      -FileFullPath (Join-Path $toolsDir 'KeyFlip.exe') `
      -Url64bit '{base}/{SC}' `
      -Checksum64 '{hashes[SC]}' -ChecksumType64 'sha256'
    '''))
print(f'generated {version} in {out}')
