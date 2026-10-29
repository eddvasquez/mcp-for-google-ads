@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

set "HUB_DIR=C:\Users\PC\Documents\ChatGPT\_ai-skills-hub"
set "PROJECT_SKILLS=%~dp0skills"

if not exist "%HUB_DIR%" (
    echo [ERROR] No se encontro el Hub central de skills en: %HUB_DIR%
    pause
    exit /b 1
)

if not exist "%PROJECT_SKILLS%" (
    mkdir "%PROJECT_SKILLS%"
)

:MENU
cls
echo ===============================================================
echo            SINCRONIZACION CON _AI-SKILLS-HUB
echo ===============================================================
echo [1] PULL - Traer skills actualizadas desde _ai-skills-hub
echo [2] PUSH - Publicar skills locales nuevas/modificadas hacia el Hub
echo [3] SALIR
echo ===============================================================
set /p OPT="Seleccione una opcion [1-3]: "

if "%OPT%"=="1" goto PULL
if "%OPT%"=="2" goto PUSH
if "%OPT%"=="3" exit /b 0
echo Opcion invalida.
pause
goto MENU

:PULL
echo.
echo Sincronizando: Hub -> Proyecto local...
robocopy "%HUB_DIR%" "%PROJECT_SKILLS%" /E /XO /XD .git /XF README.md .gitignore
echo.
echo [OK] Pull finalizado con exito.
pause
goto MENU

:PUSH
echo.
echo Sincronizando: Proyecto local -> Hub...
robocopy "%PROJECT_SKILLS%" "%HUB_DIR%" /E /XO /XD .git /XF README.md .gitignore
echo.
echo Guardando cambios en el Hub central...
pushd "%HUB_DIR%"
git add .
git commit -m "feat(skills): actualizacion de skills compartidas desde %~n0"
popd
echo [OK] Push completado exitosamente.
pause
goto MENU