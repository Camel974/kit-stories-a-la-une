# Installe le Kit Stories à la une SYSTEM (Windows). Lancer depuis le dossier du kit :
#   powershell -ExecutionPolicy Bypass -File .\installer.ps1
# Ne supprime rien. Les skills du kit sont mis à jour ; un skill externe déjà présent chez toi est gardé tel quel.
$ErrorActionPreference = 'Stop'
$kit = Split-Path -Parent $MyInvocation.MyCommand.Path
$dest = Join-Path $HOME '.claude\skills'
New-Item -ItemType Directory -Force -Path $dest | Out-Null
$maison = @('plan-a-la-une','stories-a-la-une','icones-a-la-une')

foreach ($d in Get-ChildItem (Join-Path $kit 'skills') -Directory) {
  $cible = Join-Path $dest $d.Name
  if ((Test-Path $cible) -and ($maison -notcontains $d.Name)) { Write-Host "garde   $($d.Name) (déjà installé chez toi)"; continue }
  if (Test-Path $cible) {
    Copy-Item -Path (Join-Path $d.FullName '*') -Destination $cible -Recurse -Force
    Write-Host "à jour  $($d.Name)"
  } else {
    Copy-Item -Path $d.FullName -Destination $cible -Recurse
    Write-Host "ajouté  $($d.Name)"
  }
}

$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py -or ((& python --version 2>&1) -notmatch 'Python 3')) {
  Write-Host "`n[À FAIRE] Installe Python 3 : https://www.python.org/downloads/ (coche « Add python.exe to PATH »), puis relance ce script." -ForegroundColor Yellow
} else { Write-Host "Python : OK" }
$chrome = @("$env:ProgramFiles\Google\Chrome\Application\chrome.exe", "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe", "$env:LocalAppData\Google\Chrome\Application\chrome.exe", "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe", "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe") | Where-Object { Test-Path $_ }
if (-not $chrome) { Write-Host "[À FAIRE] Installe Google Chrome : https://www.google.com/chrome/" -ForegroundColor Yellow } else { Write-Host "Navigateur : OK" }
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { Write-Host "[Optionnel, témoignages vidéo] Installe ffmpeg : winget install ffmpeg" } else { Write-Host "ffmpeg : OK" }
New-Item -ItemType Directory -Force -Path (Join-Path $kit 'mes-donnees\a-publier') | Out-Null
Write-Host "`nKit Stories à la une installé. Remplis mes-donnees\ma-marque.md, mets tes photos dans mes-donnees\photos," -ForegroundColor Green
Write-Host "puis ouvre une NOUVELLE conversation Claude Code sur ce dossier et écris : fais mes stories à la une" -ForegroundColor Green
