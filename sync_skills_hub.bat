@echo off
chcp 65001 >nul
title Sincronizador de Skills con _ai-skills-hub
set HUB_DIR=C:\Users\PC\Documents\ChatGPT\_ai-skills-hub
set LOCAL_SKILLS=%~dp0skills

echo =======================================================
echo          SINCRONIZADOR DE SKILLS CON HUB GLOBAL        
echo =======================================================
echo Hub central: %HUB_DIR%
echo Skills locales: %LOCAL_SKILLS%
echo.
echo [1] PULL - Traer/actualizar skills desde _ai-skills-hub
echo [2] PUSH - Publicar skills nuevas/modificadas hacia _ai-skills-hub
echo [3] Salir
echo.
set /p OPTION=Selecciona una opcion (1, 2 o 3): 

if "%OPTION%"=="1" goto PULL
if "%OPTION%"=="2" goto PUSH
goto END

:PULL
echo.
echo [EJECUTANDO PULL DESDE HUB...]
if not exist "%LOCAL_SKILLS%" mkdir "%LOCAL_SKILLS%"
robocopy "%HUB_DIR%" "%LOCAL_SKILLS%" /E /XO /XD .git /XF README.md .gitignore
echo.
echo Pull completado exitosamente.
goto END

:PUSH
echo.
echo [EJECUTANDO PUSH HACIA HUB...]
if not exist "%HUB_DIR%" (
    echo ERROR: No se encuentra la carpeta %HUB_DIR%
    goto END
)
robocopy "%LOCAL_SKILLS%" "%HUB_DIR%" /E /XO /XD .git /XF README.md .gitignore
echo.
echo Registrando cambios en Git de _ai-skills-hub...
pushd "%HUB_DIR%"
git add .
git status --porcelain | findstr . >nul
if %errorlevel% equ 0 (
    git commit -m "feat(skills): sincronizar skills desde proyecto local"
    echo Commit registrado en _ai-skills-hub.
) else (
    echo No hay cambios pendientes en _ai-skills-hub.
)
popd
echo.
echo Push completado exitosamente.
goto END

:END
echo.
pause