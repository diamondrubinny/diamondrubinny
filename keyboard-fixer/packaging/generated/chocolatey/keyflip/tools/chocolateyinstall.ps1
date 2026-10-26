$ErrorActionPreference = 'Stop'
$toolsDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Get-ChocolateyWebFile -PackageName 'keyflip' `
  -FileFullPath (Join-Path $toolsDir 'KeyFlip.exe') `
  -Url64bit 'https://github.com/diamondrubinny/diamondrubinny/releases/download/keyflip-v0.1.0-15/KeyFlip-windows-x64-self-contained.exe' `
  -Checksum64 '61d629f26d3bdeffc052200e1c03756516274072221f4a43544fe3213aef9d8a' -ChecksumType64 'sha256'
