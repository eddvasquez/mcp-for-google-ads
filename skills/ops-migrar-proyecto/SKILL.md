---
name: ops-migrar-proyecto
description: Ejecuta una migracion quirurgica y no-destructiva de proyectos antiguos (v1) hacia la arquitectura v2 (con Boveda Global _ai-skills-hub, utilitarios .bat y gestion de relevo), preservando intacto el estado en .context/ y el historial Git.
triggers:
  - "ops-migrar-proyecto"
  - "migrar proyecto"
  - "actualizar arquitectura"
  - "migracion v2"
---

# Skill: Migración No-Destructiva de Proyectos (`ops-migrar-proyecto`)

## Propósito y Alcance
Actualiza cualquier proyecto existente dentro de `C:\Users\PC\Documents\ChatGPT\<proyecto>` a la arquitectura v2 sin sobrescribir ni alterar el avance, los entregables ni la memoria activa del proyecto.

- **Regla de Oro (Modo No-Destructivo):** Está ESTRICTAMENTE PROHIBIDO modificar, truncar o sobrescribir `.context/projectbrief.md`, `.context/activeContext.md`, `.context/progress.md`, `.context/systemPatterns.md`, `docs/sop_gtm_governance.md` o cualquier archivo de trabajo existente.

---

## FASE 1: CUESTIONARIO BLOQUEANTE DE DESCUBRIMIENTO
Al activarse esta skill, detente y haz ÚNICAMENTE estas 2 preguntas al usuario:

1. **Proyecto(s) a migrar:** Indica el nombre exacto de la carpeta dentro de `C:\Users\PC\Documents\ChatGPT\` (o escribe `"TODOS"` si quieres un script que recorra y migre todas tus carpetas de proyectos existentes en lote).
2. **Modo de ejecución:** ¿Prefieres **A)** que te entregue los bloques de código (`migrate_project.ps1` y `migrate_project.bat`) listos para ejecutar con doble clic, o **B)** (si estás en Antigravity/Claude con acceso local) que ejecute la migración directamente en disco?

---

## FASE 2: REGLAS TÉCNICAS DE EJECUCIÓN (TRAS RECIBIR RESPUESTAS)

1. **Seguridad en PowerShell y .NET:**
   - Usar `$ErrorActionPreference = "Stop"`, sincronizar `[System.Environment]::CurrentDirectory = (Get-Location).Path` y escribir archivos nuevos exclusivamente con `[System.Text.UTF8Encoding]::new($false)` (UTF-8 sin BOM) y Here-Strings literales (`@' ... '@`).
   - Si se eligió migrar `"TODOS"`, excluir explícitamente la carpeta `_ai-skills-hub` del bucle de proyectos.

2. **Resguardo Previo del Árbol Git Local:**
   - Mantener la carpeta `.git` nativa dentro del proyecto (si no existiera `.git`, inicializarla con `git init`).
   - Configurar de inmediato las protecciones para Google Drive:
     * `git config core.fscache true`
     * `git config core.preloadindex true`
     * `git config core.longpaths true`
   - Si `git status --porcelain` muestra cambios previos sin guardar antes de iniciar la migración, realizar primero un commit de resguardo: `git add .` -> `Start-Sleep -Milliseconds 800` -> `git commit -m "chore(backup): snapshot pre-migration v1 state"`.

3. **Inyección de Componentes Nuevos (Idempotente):**
   - Crear `.context/lessons_learned.md` ÚNICAMENTE si no existe aún en el proyecto.
   - Crear la carpeta `./skills/` en el proyecto si no existe y copiar dentro las subcarpetas de `C:\Users\PC\Documents\ChatGPT\_ai-skills-hub` excluyendo estrictamente `.git`, `README.md` y `.gitignore` del Hub.
   - Generar en la raíz del proyecto (iniciando con `chcp 65001 >nul`):
     * `sync_skills_hub.bat`: Menú `[1] PULL (Traer skills desde _ai-skills-hub)` y `[2] PUSH (Publicar skills nuevas hacia _ai-skills-hub y hacer commit en el Hub)` con `robocopy /E /XO /XD .git /XF README.md .gitignore`.
     * `copy_context_for_chat.bat`: Empaqueta `AGENTS.md`, `.context/*`, listado de `skills/` y `git status -s` al portapapeles (`Set-Clipboard`).

4. **Actualización con Respaldo Único de `AGENTS.md`:**
   - Si existe `AGENTS.md` y todavía NO existe `.context/AGENTS.v1.bak`, copiar el `AGENTS.md` actual hacia `.context/AGENTS.v1.bak` para preservar cualquier nota antigua.
   - Escribir el nuevo `AGENTS.md` en la raíz con los 5 protocolos completos:
     * **Protocolo 1 (Inicio de Sesión y Auditoría Git):** Ejecutar `skills/ops-gestion-relevo/SKILL.md` en `MODO ENTRADA`. Prevalece Git sobre `activeContext.md`.
     * **Protocolo 2 (Cero Suposiciones y Memoria Cruda):** Prohibido adivinar; registrar toda corrección en `.context/lessons_learned.md`.
     * **Protocolo 3 (Destilación Controlada a Skill General):** Prohibido modificar `skills/` sin aprobación humana explícita. Abstraer reglas universales con prefijo (`dev-`, `gtm-`, `ads-`, `copy-`, `ops-`) en `skills/<prefijo-nombre>/SKILL.md`, limpiar `lessons_learned.md` tras confirmar e indicar el uso de `sync_skills_hub.bat`.
     * **Protocolo 4 (Escritor Único e Higiene en Google Drive):** Prohibido crear sufijos `_v1` o `_final`; advertir antes de instalar `node_modules` o `.venv`.
     * **Protocolo 5 (Cierre de Turno / Handoff):** Ejecutar `skills/ops-gestion-relevo/SKILL.md` en `MODO SALIDA`.

5. **Actualización de `.gitignore` y Commit de Migración:**
   - Añadir al final de `.gitignore` (solo si no están presentes ya): `migrate_project.*`, `setup_project.*`, `desktop.ini`, `Thumbs.db`, `.DS_Store`, `.env`, `node_modules/`, `.venv/`.
   - Ejecutar `git add .`, esperar `Start-Sleep -Milliseconds 800` y ejecutar:
     `git commit -m "chore(arch): migrar proyecto a arquitectura v2 con skills hub y gestion de relevo"`