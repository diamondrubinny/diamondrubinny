$ErrorActionPreference = 'Stop'
$toolsDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Get-ChocolateyWebFile -PackageName 'keyflip' `
  -FileFullPath (Join-Path $toolsDir 'KeyFlip.exe') `
  -Url64bit 'https://github.com/diamondrubinny/diamondrubinny/releases/download/keyflip-v0.1.0-24/KeyFlip-windows-x64-self-contained.exe' `
  -Checksum64 '6b3b810a17e8dd310037286ae4f44e220c64273cdca0f64ab73711f1cf93782b' -ChecksumType64 'sha256'
