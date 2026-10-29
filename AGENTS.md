# Protocolo de Operación de Agentes — Arquitectura v2 centralizada

## Protocolo 1 — Entrada y auditoría
Ejecutar C:\Users\PC\Documents\ChatGPT\_ai-skills-hub\ops-gestion-relevo\SKILL.md en MODO ENTRADA. Leer AGENTS.md y los cinco archivos de .context/. Listar las skills de C:\Users\PC\Documents\ChatGPT\_ai-skills-hub. Auditar git status -s, git log -n 3 --oneline y git diff --stat. Prevalece Git ante discrepancias. Entregar el reporte de cinco puntos y esperar confirmación antes de escribir, salvo autorización explícita vigente para el trabajo solicitado.

## Protocolo 2 — Requisitos y memoria
No inventar requisitos, dependencias ni credenciales. Preguntar ante datos críticos ausentes. Registrar correcciones permanentes con fecha, error y regla en .context/lessons_learned.md. Consultar las skills exclusivamente en C:\Users\PC\Documents\ChatGPT\_ai-skills-hub; para Google Ads usar google-ads-media-buyer/SKILL.md dentro de esa Bóveda.

## Protocolo 3 — Skills generales
No crear ni modificar skills sin autorización humana explícita. Proponer la destilación de reglas reutilizables y, tras aprobación, escribir exclusivamente en C:\Users\PC\Documents\ChatGPT\_ai-skills-hub\<prefijo-nombre>\SKILL.md con YAML name, description y triggers. Usar prefijos dev-, gtm-, ads-, copy- u ops-. Verificar y registrar los cambios con Git en la Bóveda antes de depurar la regla equivalente de lessons_learned.md. No crear skills locales ni sincronizadores.

## Protocolo 4 — Escritor único e higiene
Validar Agente Activo en .context/activeContext.md antes de escribir. Prohibidos duplicados con sufijos _v01, _v1, _v2, _final, _WIP o _backup; usar commits atómicos. Solicitar confirmación antes de instalar dependencias masivas o descargas pesadas. Fuente única de skills: C:\Users\PC\Documents\ChatGPT\_ai-skills-hub.

## Protocolo 5 — Salida
Ejecutar C:\Users\PC\Documents\ChatGPT\_ai-skills-hub\ops-gestion-relevo\SKILL.md en MODO SALIDA. Actualizar lessons_learned.md cuando corresponda, progress.md solo con hitos comprobados y activeContext.md con el último cambio, errores y siguiente paso exacto. Confirmar commits de skills autorizadas en la Bóveda. En el proyecto, git add -A, esperar un segundo y realizar el commit de relevo, usando el mensaje específico del usuario cuando lo haya indicado. Verificar git status -s al finalizar.