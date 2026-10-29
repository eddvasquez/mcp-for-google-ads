@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Empaquetador de Contexto para Chat
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command ^
  "$output = New-Object System.Text.StringBuilder; " ^
  "[void]$output.AppendLine('==================== AGENTS.MD ===================='); " ^
  "if (Test-Path 'AGENTS.md') { [void]$output.AppendLine((Get-Content 'AGENTS.md' -Raw)) }; " ^
  "[void]$output.AppendLine('`n==================== CONTEXTO (.context/*) ===================='); " ^
  "if (Test-Path '.context') { Get-ChildItem '.context' -File | ForEach-Object { [void]$output.AppendLine('--- ' + $_.Name + ' ---'); [void]$output.AppendLine((Get-Content $_.FullName -Raw)); [void]$output.AppendLine('') } }; " ^
  "[void]$output.AppendLine('==================== SKILLS DISPONIBLES ===================='); " ^
  "if (Test-Path '..\_ai-skills-hub') { Get-ChildItem '..\_ai-skills-hub' -Directory | ForEach-Object { [void]$output.AppendLine('- ' + $_.Name) } }; " ^
  "[void]$output.AppendLine('`n==================== GIT STATUS ===================='); " ^
  "if (Test-Path '.git') { [void]$output.AppendLine((git status -s)) }; " ^
  "$output.ToString() | Set-Clipboard; " ^
  "Write-Host 'Contexto completo copiado exitosamente al portapapeles!' -ForegroundColor Green"
echo.
pause