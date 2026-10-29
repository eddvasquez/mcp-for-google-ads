# Protocolo de Operación de Agentes (Arquitectura v2)

Todo agente o modelo de IA que opere en este repositorio debe cumplir de forma estricta e innegociable con los siguientes protocolos:

---

### Protocolo 1 (Inicio de Sesión y Auditoría Git)
- Al iniciar cualquier turno sobre el proyecto, es mandatorio ejecutar la skill ubicada en `skills/ops-gestion-relevo/SKILL.md` bajo **MODO ENTRADA**.
- Lee `AGENTS.md`, todos los archivos de `.context/` (`projectbrief.md`, `systemPatterns.md`, `activeContext.md`, `progress.md`, `lessons_learned.md`) y lista las carpetas dentro de `skills/`.
- Ejecuta una auditoría física en Git (`git status -s`, `git log -n 3 --oneline`).
- **Resolución de discrepancias:** En caso de existir cualquier contradicción entre el texto de `.context/activeContext.md` y el estado real del árbol de trabajo en Git, **prevalece siempre la evidencia física de Git**.
- Emite el reporte de sincronización de 5 puntos y detente a esperar la confirmación del usuario antes de tocar archivos.

---

### Protocolo 2 (Cero Suposiciones y Memoria Cruda)
- Está terminantemente prohibido adivinar requerimientos, suponer dependencias o inventar credenciales.
- Cuando falte información crítica o existan ambigüedades, formula preguntas concisas y bloqueantes.
- Toda corrección, rechazo de enfoque o directriz permanente expresada por el usuario debe registrarse de inmediato en `.context/lessons_learned.md` con fecha, error original y regla corregida.

---

### Protocolo 3 (Destilación Controlada a Skill General)
- Está estrictamente prohibido modificar o crear archivos dentro de `skills/` sin la autorización humana explícita.
- Cuando una solución o regla documentada en `.context/lessons_learned.md` demuestre ser universalmente reutilizable para otros proyectos, el agente debe proponer formalmente al usuario su destilación como Skill Global.
- Tras la aprobación del usuario, se abstrae en `skills/<prefijo-nombre>/SKILL.md` utilizando prefijos canónicos (`dev-`, `gtm-`, `ads-`, `copy-`, `ops-`) con cabecera YAML estandarizada (`name`, `description`, `triggers`).
- Una vez verificada la nueva skill, se depura la regla equivalente de `.context/lessons_learned.md` y se recuerda al usuario ejecutar `sync_skills_hub.bat` (Opción 2 - PUSH) para propagarla a `_ai-skills-hub`.

---

### Protocolo 4 (Escritor Único e Higiene en Google Drive)
- **Principio de escritor único:** Validar que el campo `Agente Activo` en `.context/activeContext.md` coincida con la plataforma actual antes de efectuar escrituras.
- **Prohibición de duplicados:** Estrictamente prohibido crear archivos con sufijos de versionado (`_v01`, `_v2`, `_final`, `_WIP`, `_backup`). Toda iteración se versiona exclusivamente mediante commits atómicos de Git.
- **Higiene y rendimiento en carpetas sincronizadas:** Advertir y solicitar confirmación previa antes de instalar dependencias masivas locales (`node_modules/`, carpetas virtuales `.venv/`, o descargas pesadas) para no degradar la sincronización en nube.

---

### Protocolo 5 (Cierre de Turno / Handoff)
- Al concluir cualquier unidad de trabajo o antes de devolver el control al usuario, el agente debe ejecutar obligatoriamente `skills/ops-gestion-relevo/SKILL.md` bajo **MODO SALIDA**.
- Actualizar `.context/lessons_learned.md` si hubo aprendizajes o correcciones.
- Actualizar `.context/progress.md` marcando con `[x]` únicamente hitos comprobados objetivamente.
- Actualizar `.context/activeContext.md` indicando con precisión quirúrgica: último archivo modificado, estado de revisión/errores y el siguiente paso ejecutable inmediato para el próximo relevo.
- Realizar el commit atómico de relevo: `git add .` -> esperar 1 segundo para liberar bloqueos de Google Drive -> `git commit -m "chore(relevo): actualizar activeContext y progreso de sesion"`.
- *Una vez actualizado activeContext y efectuado el commit, el agente no debe ejecutar código adicional en ese turno.*