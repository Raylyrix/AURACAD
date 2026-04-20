# AuraCAD Rebranding Script - PowerShell

$SourcePath = "C:\Users\hp\Desktop\PHYSICALCAD\AuraCAD\src"
$WhatIf = $false

$patterns = @(
    @{ find = "FreeCAD"; replace = "AuraCAD" },
    @{ find = "freecad"; replace = "auracad" },
    @{ find = "FREECAD"; replace = "AURACAD" },
    @{ find = "FreeCADGui"; replace = "AuraCADGui" },
    @{ find = "FreeCADStd"; replace = "AuraCADStd" },
    @{ find = "QtFreeCAD"; replace = "AuraCAD" },
    @{ find = "fc_std"; replace = "auracad_std" },
    @{ find = "FreeCAD.py"; replace = "AuraCAD.py" },
    @{ find = "FreeCAD.xml"; replace = "AuraCAD.xml" },
    @{ find = "FREECAD_LIB"; replace = "AURACAD_LIB" },
    @{ find = "FREECAD_HOME"; replace = "AURACAD_HOME" },
    @{ find = "/freecad"; replace = "/auracad" },
    @{ find = "libFreeCAD"; replace = "libAuraCAD" },
    @{ find = "QtGui:/freecad"; replace = "QtGui:/auracad" },
    @{ find = "org.freecad"; replace = "org.auracad" },
    @{ find = "org.freecad.FreeCAD"; replace = "org.auracad.AuraCAD" },
    @{ find = "FC_"; replace = "AuraCAD_" },
    @{ find = "fc"; replace = "auracad" }
)

$Extensions = @("*.cpp", "*.h", "*.py", "*.xml", "*.qrc", "*.ts", "*.cfg", "CMakeLists.txt", "*.txt", "*.md", "*.ad", "*.in", "*.ui", "*.qtm", "*.hpp", "*.cc")

Write-Host "=== AuraCAD Rebranding ===" -ForegroundColor Cyan

$Files = Get-ChildItem -Path $SourcePath -Recurse -File -Include $Extensions | Where-Object { $_.FullName -notlike "*\.git*" -and $_.FullName -notlike "*node_modules*" }

$Total = $Files.Count
$Processed = 0
$Modified = 0

foreach ($File in $Files) {
    $Processed++
    if ($Processed % 1000 -eq 0) {
        Write-Host "Progress: $Processed / $Total" -ForegroundColor Yellow
    }

    $Content = Get-Content $File.FullName -Raw -ErrorAction SilentlyContinue
    if ($null -eq $Content) { continue }

    $Original = $Content

    foreach ($p in $patterns) {
        $Content = $Content -replace [regex]::Escape($p.find), $p.replace
    }

    if ($Content -ne $Original) {
        if (-not $WhatIf) {
            Set-Content -Path $File.FullName -Value $Content -NoNewline -Encoding UTF8
        }
        $Modified++
    }
}

Write-Host ""
Write-Host "=== Complete ===" -ForegroundColor Green
Write-Host "Files modified: $Modified of $Total"

# Rename directories and key files
$Renames = Get-ChildItem -Path $SourcePath -Directory -Recurse | Where-Object { $_.Name -like "*freecad*" }
foreach ($dir in $Renames) {
    $new = $dir.FullName -replace "freecad", "auracad"
    Write-Host "Would rename: $($dir.Name) -> $(Split-Path $new -Leaf)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Now run build instructions:" -ForegroundColor Cyan
Write-Host "1. cd AuraCAD\src"
Write-Host "2. mkdir build && cd build"
Write-Host "3. cmake .. -G 'Ninja'"
Write-Host "4. cmake --build . --config Release"
Write-Host "5. ./bin/AuraCAD"