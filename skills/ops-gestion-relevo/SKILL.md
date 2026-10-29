---
name: ops-gestion-relevo
description: Protocolo determinista de Recepción (Modo ENTRADA) y Cierre de Turno (Modo SALIDA) para garantizar continuidad sin pérdida de estado ni corrupción de archivos entre Google Antigravity, Claude y ChatGPT.
triggers:
  - "ops-gestion-relevo"
  - "inicia turno"
  - "relevo de entrada"
  - "modo entrada"
  - "cierra turno"
  - "relevo de salida"
  - "modo salida"
---

# Skill: Gestión de Relevo Multi-Agente (Entrada y Salida)

## Propósito y Alcance
Esta skill gobierna la apertura y el cierre de sesiones de trabajo cuando un proyecto es operado secuencialmente por distintas IAs.
- **Cuándo usar:** Obligatoriamente al abrir una nueva sesión sobre un proyecto existente (`Modo ENTRADA`) y antes de cerrar la sesión actual (`Modo SALIDA`).
- **Restricción absoluta:** En `Modo ENTRADA` está ESTRICTAMENTE PROHIBIDO modificar archivos o escribir código funcional antes de que el usuario apruebe el Reporte de Sincronización.

---

## MODO A: RECEPCIÓN DE TURNO (`MODO ENTRADA`)

### Procedimiento Paso a Paso
1. **Lectura de Contexto:** Lee `AGENTS.md` y todos los archivos dentro de `.context/` (`projectbrief.md`, `systemPatterns.md`, `activeContext.md`, `progress.md`, `lessons_learned.md`).
2. **Escaneo de Capacidades:** Lista las subcarpetas dentro de `skills/` para identificar qué procedimientos estandarizados están instalados en el proyecto.
3. **Auditoría Física en Git:** Ejecuta (o solicita si no tienes terminal) `git status -s`, `git log -n 3 --oneline` y, si existen archivos modificados sin commit, `git diff --stat`.
4. **Resolución de Discrepancias:** Compara `activeContext.md` contra la salida de Git. Si la sesión anterior se interrumpió sin actualizar el Markdown, **prevalece la evidencia física de Git**.

### Entregable Obligatorio (Detenerse tras responder)
Entrega ÚNICAMENTE este reporte de 5 puntos y espera el "OK" del usuario:
1. **Auditoría Git vs. Contexto:** Estado del árbol de trabajo y si coincide o no con `activeContext.md`.
2. **Reglas y Bloqueos Activos:** Las 2-3 restricciones clave de `systemPatterns.md` / `lessons_learned.md` aplicables hoy (indicando si existe `[BLOQUEO ACTIVO]` de stack).
3. **Skills Aplicables:** Qué `SKILL.md` de la carpeta `skills/` se usará en la tarea actual.
4. **Siguiente Paso Ejecutable:** En una frase, qué acción exacta realizarás y qué archivo tocarás tras recibir autorización.
5. **Dudas Bloqueantes:** Preguntas concisas si falta algún dato crítico (prohibido adivinar).

---

## MODO B: CIERRE DE TURNO (`MODO SALIDA`)

### Procedimiento Paso a Paso
1. **Captura en Memoria Cruda (`.context/lessons_learned.md`):** Si durante la sesión el usuario corrigió entregables, rechazó un enfoque o fijó una regla permanente, regístralo al final de `lessons_learned.md` con fecha, error original y regla corregida. *(Prohibido crear o editar archivos en `skills/` sin autorización explícita).*
2. **Actualización de Hitos (`.context/progress.md`):** Marca con `[x]` exclusivamente los entregables 100% terminados y verificados en la sesión.
3. **Actualización de Estado (`.context/activeContext.md`):** Sobrescribe el estado actual especificando con precisión quirúrgica:
   - Qué se completó exactamente en esta sesión.
   - En qué archivo/línea quedó el trabajo y qué bloqueos existen.
   - Cuál es el **Siguiente paso ejecutable exacto** para el próximo agente.
4. **Commit Atómico Anti-Bloqueo (Google Drive Safe):**
   - Ejecuta `git status -s`.
   - Ejecuta `git add .`, espera al menos 1 segundo para que Google Drive libere `.git/index.lock`, y ejecuta:
     `git commit -m "chore(relevo): actualizar activeContext y progreso de sesion"`

### Checklist de Autovalidación antes de despedirse
- [ ] ¿`activeContext.md` refleja la verdad exacta de `git status`?
- [ ] ¿Se respetó la prohibición de no crear archivos `_v1` o `_final`?
- [ ] ¿El commit se realizó sin errores de `.git/index.lock`?