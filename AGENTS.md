# Protocolo de OperaciÃ³n de Agentes (Arquitectura v2)

Todo agente o modelo de IA que opere en este repositorio debe cumplir de forma estricta e innegociable con los siguientes protocolos:

---

### Protocolo 1 (Inicio de SesiÃ³n y AuditorÃ­a Git)
- Al iniciar cualquier turno sobre el proyecto, es mandatorio ejecutar la skill ubicada en `skills/ops-gestion-relevo/SKILL.md` bajo **MODO ENTRADA**.
- Lee `AGENTS.md`, todos los archivos de `.context/` (`projectbrief.md`, `systemPatterns.md`, `activeContext.md`, `progress.md`, `lessons_learned.md`) y lista las carpetas dentro de `skills/`.
- Ejecuta una auditorÃ­a fÃ­sica en Git (`git status -s`, `git log -n 3 --oneline`).
- **ResoluciÃ³n de discrepancias:** En caso de existir cualquier contradicciÃ³n entre el texto de `.context/activeContext.md` y el estado real del Ã¡rbol de trabajo en Git, **prevalece siempre la evidencia fÃ­sica de Git**.
- Emite el reporte de sincronizaciÃ³n de 5 puntos y detente a esperar la confirmaciÃ³n del usuario antes de tocar archivos.

---

### Protocolo 2 (Cero Suposiciones y Memoria Cruda)
- EstÃ¡ terminantemente prohibido adivinar requerimientos, suponer dependencias o inventar credenciales.
- Cuando falte informaciÃ³n crÃ­tica o existan ambigÃ¼edades, formula preguntas concisas y bloqueantes.
- Toda correcciÃ³n, rechazo de enfoque o directriz permanente expresada por el usuario debe registrarse de inmediato en `.context/lessons_learned.md` con fecha, error original y regla corregida.

---

### Protocolo 3 (DestilaciÃ³n Controlada a Skill General)
- EstÃ¡ estrictamente prohibido modificar o crear archivos dentro de `skills/` sin la autorizaciÃ³n humana explÃ­cita.
- Cuando una soluciÃ³n o regla documentada en `.context/lessons_learned.md` demuestre ser universalmente reutilizable para otros proyectos, el agente debe proponer formalmente al usuario su destilaciÃ³n como Skill Global.
- Tras la aprobaciÃ³n del usuario, se abstrae en `skills/<prefijo-nombre>/SKILL.md` utilizando prefijos canÃ³nicos (`dev-`, `gtm-`, `ads-`, `copy-`, `ops-`) con cabecera YAML estandarizada (`name`, `description`, `triggers`).
- Una vez verificada la nueva skill, se depura la regla equivalente de `.context/lessons_learned.md` y se recuerda al usuario ejecutar `sync_skills_hub.bat` (OpciÃ³n 2 - PUSH) para propagarla a `_ai-skills-hub`.

---

### Protocolo 4 (Escritor Ãšnico e Higiene en Google Drive)
- **Principio de escritor Ãºnico:** Validar que el campo `Agente Activo` en `.context/activeContext.md` coincida con la plataforma actual antes de efectuar escrituras.
- **ProhibiciÃ³n de duplicados:** Estrictamente prohibido crear archivos con sufijos de versionado (`_v01`, `_v2`, `_final`, `_WIP`, `_backup`). Toda iteraciÃ³n se versiona exclusivamente mediante commits atÃ³micos de Git.
- **Higiene y rendimiento en carpetas sincronizadas:** Advertir y solicitar confirmaciÃ³n previa antes de instalar dependencias masivas locales (`node_modules/`, carpetas virtuales `.venv/`, o descargas pesadas) para no degradar la sincronizaciÃ³n en nube.

---

### Protocolo 5 (Cierre de Turno / Handoff)
- Al concluir cualquier unidad de trabajo o antes de devolver el control al usuario, el agente debe ejecutar obligatoriamente `skills/ops-gestion-relevo/SKILL.md` bajo **MODO SALIDA**.
- Actualizar `.context/lessons_learned.md` si hubo aprendizajes o correcciones.
- Actualizar `.context/progress.md` marcando con `[x]` Ãºnicamente hitos comprobados objetivamente.
- Actualizar `.context/activeContext.md` indicando con precisiÃ³n quirÃºrgica: Ãºltimo archivo modificado, estado de revisiÃ³n/errores y el siguiente paso ejecutable inmediato para el prÃ³ximo relevo.
- Realizar el commit atÃ³mico de relevo: `git add .` -> esperar 1 segundo para liberar bloqueos de Google Drive -> `git commit -m "chore(relevo): actualizar activeContext y progreso de sesion"`.
- *Una vez actualizado activeContext y efectuado el commit, el agente no debe ejecutar cÃ³digo adicional en ese turno.*