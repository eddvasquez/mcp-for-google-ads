---
name: ops-crear-proyecto
description: Inicializa la arquitectura local determinista de un nuevo proyecto en C:\Users\PC\Documents\ChatGPT\<nombre>, aprovisionando .context/, skills/, docs/, AGENTS.md y Git protegido para Google Drive.
triggers:
  - "ops-crear-proyecto"
  - "crear nuevo proyecto"
  - "inicializar proyecto"
  - "nuevo proyecto"
---

# Skill: Inicializador de Arquitectura de Proyecto (`ops-crear-proyecto`)

## Propósito y Alcance
Crea desde cero la estructura estandarizada de un proyecto multi-agente dentro de `C:\Users\PC\Documents\ChatGPT\`.
- **Restricción de Fase 1:** NUNCA generes scripts ni crees carpetas sin antes formular las 4 preguntas de descubrimiento y recibir respuesta del usuario.

---

## FASE 1: CUESTIONARIO BLOQUEANTE DE DESCUBRIMIENTO
Al activarse esta skill, detente y formula ÚNICAMENTE estas 4 preguntas al usuario:

1. **Nombre del proyecto (formato `kebab-case` sin tildes ni espacios, se creará en `C:\Users\PC\Documents\ChatGPT\<nombre>`):**
2. **Objetivo principal y entregable esperado:**
3. **Stack o tecnologías clave (elige A, B o C):**
   - **A) Por Ecosistema/Plataformas:** (Ej: WordPress + GTM + JS Vanilla | Google Ads + GA4 + Data Layer).
   - **B) Por Entregable Técnico:** (Ej: Scripts PowerShell | Automatización Python/Node | Landing HTML/CSS).
   - **C) "Por definir (Requiere evaluación técnica)":** Fase exploratoria (activa bloqueo de código hasta aprobar arquitectura).
4. **¿El proyecto incluye Analítica Web, Tag Management (GTM) o Tráfico Pago? (Sí / No):**

---

## FASE 2: EJECUCIÓN O GENERACIÓN DE SCRIPTS (TRAS RECIBIR RESPUESTAS)

### Regla de Enrutamiento según Capacidad del Agente:
- **Si tienes acceso de escritura y terminal local (ej. Antigravity / Claude con MCP activo en `C:\Users\PC\Documents\ChatGPT`):** Aprovisiona directamente la estructura en disco cumpliendo todos los Requisitos Técnicos de abajo, incluyendo los archivos utilitarios `.bat`.
- **Si operas solo en interfaz de chat sin acceso directo al disco:** Entrega ÚNICAMENTE los 4 bloques de código listos para copiar (`setup_project.ps1`, `setup_project.bat`, `sync_skills_hub.bat` y `copy_context_for_chat.bat`) sin explicaciones teóricas.

### Requisitos Técnicos Obligatorios de Aprovisionamiento:
1. **Rutas y Codificación (.NET Safe):**
   - `$WorkspaceRoot = "C:\Users\PC\Documents\ChatGPT"`
   - `$ProjectPath = Join-Path $WorkspaceRoot "<nombre-del-proyecto>"`
   - `$SkillsHubPath = Join-Path $WorkspaceRoot "_ai-skills-hub"`
   - Sincronizar siempre `[System.Environment]::CurrentDirectory = (Get-Location).Path`.
   - Escribir todo archivo con `[System.Text.UTF8Encoding]::new($false)` y Here-Strings literales de comillas simples (`@' ... '@`).
2. **Estructura, Herencia de Skills y Git Nativo (Google Drive Safe):**
   - Crear carpetas `.context/`, `skills/` y `docs/`.
   - Copiar las subcarpetas de `$SkillsHubPath` hacia `$ProjectPath\skills\` excluyendo estrictamente `.git`, `README.md` y `.gitignore` del Hub.
   - Ejecutar `git init` local en `$ProjectPath` y configurar `core.fscache true`, `core.preloadindex true` y `core.longpaths true`.
   - Crear `.gitignore` excluyendo `.env`, `node_modules/`, `.venv/`, `*.log`, `.DS_Store`, `Thumbs.db`, `desktop.ini`, `setup_project.*`.
3. **Archivos de `.context/` y Bifurcación de Stack:**
   - Generar `projectbrief.md`, `systemPatterns.md`, `activeContext.md`, `progress.md` y `lessons_learned.md`.
   - Si el Stack es **A o B**: Estado `DESBLOQUEADO PARA DESARROLLO`. Siguiente paso: rama `feature/initial-setup`.
   - Si el Stack es **C ("Por definir")**: Insertar `[BLOQUEO ACTIVO]` en `systemPatterns.md` prohibiendo escribir código funcional hasta aprobar una tabla comparativa de 2-3 opciones de stack.
   - Si la Pregunta 4 fue **"Sí"** (o Stack C): Generar `docs/sop_gtm_governance.md`.
4. **Gobernanza en `AGENTS.md` (Referencias Exactas en Español):**
   - Incluir los 5 protocolos completos:
     * **Protocolo 1 (Inicio de Sesión y Auditoría Git):** Instruir al agente a ejecutar `skills/ops-gestion-relevo/SKILL.md` en **MODO ENTRADA**.
     * **Protocolo 2 (Cero Suposiciones y Memoria Cruda):** Prohibido adivinar; registrar toda corrección en `.context/lessons_learned.md`.
     * **Protocolo 3 (Destilación Controlada a Skill):** Prohibido tocar `skills/` sin permiso explícito; abstraer reglas universales con prefijo (`dev-`, `gtm-`, `ads-`, `copy-`, `ops-`) en `skills/<prefijo-nombre>/SKILL.md`, limpiar `lessons_learned.md` tras confirmar y recordar usar `sync_skills_hub.bat`.
     * **Protocolo 4 (Escritor Único e Higiene en Google Drive):** Prohibido crear sufijos `_v1` o `_final`; advertir antes de instalar dependencias masivas (`node_modules`/`.venv`).
     * **Protocolo 5 (Cierre de Turno / Handoff):** Instruir al agente a ejecutar `skills/ops-gestion-relevo/SKILL.md` en **MODO SALIDA**.
5. **Utilitarios Batch (Con `chcp 65001 >nul`) y Commit Inicial:**
   - Generar `sync_skills_hub.bat` (iniciando con `chcp 65001 >nul` y menú `[1] PULL` y `[2] PUSH` usando `robocopy /E /XO /XD .git /XF README.md .gitignore`) y `copy_context_for_chat.bat` (`Set-Clipboard`).
   - Ejecutar `git add .`, esperar `Start-Sleep -Milliseconds 800` y ejecutar `git commit -m "chore: initialize project architecture, memory bank and skills hub"`.