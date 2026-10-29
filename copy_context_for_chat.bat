@echo off
chcp 65001 >nul
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "& {
    $output = [System.Text.StringBuilder]::new()
    [void]$output.AppendLine('=== ESTADO DEL REPOSITORIO (git status -s) ===')
    $gitStatus = git status -s 2>&1
    [void]$output.AppendLine(($gitStatus -join [Environment]::NewLine))
    [void]$output.AppendLine('')

    if (Test-Path 'AGENTS.md') {
        [void]$output.AppendLine('=== ARCHIVO: AGENTS.md ===')
        [void]$output.AppendLine([System.IO.File]::ReadAllText('AGENTS.md', [System.Text.Encoding]::UTF8))
        [void]$output.AppendLine('')
    }

    if (Test-Path '.context') {
        Get-ChildItem -Path '.context' -File | ForEach-Object {
            [void]$output.AppendLine(\"=== ARCHIVO: .context/$($_.Name) ===\")
            [void]$output.AppendLine([System.IO.File]::ReadAllText($_.FullName, [System.Text.Encoding]::UTF8))
            [void]$output.AppendLine('')
        }
    }

    if (Test-Path 'skills') {
        [void]$output.AppendLine('=== SKILLS DISPONIBLES EN PROYECTO ===')
        Get-ChildItem -Path 'skills' -Directory | ForEach-Object {
            [void]$output.AppendLine(\"- $($_.Name)\")
        }
        [void]$output.AppendLine('')
    }

    $finalText = $output.ToString()
    Set-Clipboard -Value $finalText
    Write-Host '[OK] Contexto consolidado copiado al portapapeles exitosamente.' -ForegroundColor Green
}"
pause