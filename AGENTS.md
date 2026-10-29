# AGENTS.md - Protocolos de OperaciÃ³n y Memoria del Agente (Arquitectura v2)

Este proyecto opera bajo una arquitectura de relevo estricto, memoria versionada y modularizaciÃ³n de capacidades mediante Skills. Todo agente de Inteligencia Artificial debe adherirse rigurosamente a los siguientes protocolos.

---

### Protocolo 1: Inicio de SesiÃ³n y AuditorÃ­a Git
1. **EjecuciÃ³n de Relevo Entrante:** Al iniciar cualquier interacciÃ³n o turno de trabajo, el agente debe consultar e invocar `skills/ops-gestion-relevo/SKILL.md` en **MODO ENTRADA**.
2. **JerarquÃ­a de la Verdad:** El estado real del repositorio (`git status`, `git log -n 5`) prevalece siempre sobre cualquier archivo estÃ¡tico o resumen previo en `.context/activeContext.md`.
3. **AuditorÃ­a Inicial:** Verificar si existen cambios pendientes sin commitear antes de proponer modificaciones en el cÃ³digo o documentaciÃ³n.

---

### Protocolo 2: Cero Suposiciones y Memoria Cruda
1. **ProhibiciÃ³n de Adivinar:** Si faltan credenciales, variables de entorno, rutas o definiciones de negocio, el agente debe detenerse y preguntar explÃ­citamente en lugar de inferir o crear datos ficticios.
2. **Registro de Correcciones:** Toda retroalimentaciÃ³n correctiva por parte del usuario, error recurrente, preferencia operativa o regla especÃ­fica del proyecto debe ser documentada de inmediato en `.context/lessons_learned.md`.

---

### Protocolo 3: DestilaciÃ³n Controlada a Skill General
1. **Aislamiento de Skills:** Queda estrictamente prohibido crear, modificar o eliminar archivos dentro de la carpeta `skills/` sin la autorizaciÃ³n humana explÃ­cita previa.
2. **AbstracciÃ³n:** Cuando un flujo o regla documentada en `.context/lessons_learned.md` demuestre ser universal, estructurarla como una nueva Skill con su prefijo semÃ¡ntico correspondiente:
   - `dev-`: Flujos de desarrollo de software, arquitectura o scripts.
   - `gtm-`: Estrategias Go-To-Market, tracking y analÃ­tica.
   - `ads-`: Operaciones en plataformas publicitarias (Google Ads, Meta Ads).
   - `copy-`: RedacciÃ³n persuasiva, frameworks de mensajerÃ­a y VSL.
   - `ops-`: Procedimientos operativos estÃ¡ndar, gobernanza y relevo.
3. **Estructura EstÃ¡ndar de Skill:** Cada habilidad debe residir en `skills/<prefijo-nombre>/SKILL.md` conteniendo cabecera YAML obligatoria (`name`, `description`, `triggers`).
4. **SincronizaciÃ³n:** Una vez aprobada y refinada la skill, purgar la regla redundante de `lessons_learned.md` y solicitar al usuario la ejecuciÃ³n de `sync_skills_hub.bat` para propagarla a `_ai-skills-hub`.

---

### Protocolo 4: Escritor Ãšnico e Higiene en Google Drive
1. **ProhibiciÃ³n de Sufijos:** Queda estrictamente prohibido generar archivos con sufijos de versiÃ³n o estado (ej. `_v1`, `_v2`, `_final`, `_backup`, `_copia`). Toda evoluciÃ³n debe ser gobernada por Git.
2. **PrevenciÃ³n de Bloqueos:** Advertir y confirmar antes de inicializar dependencias masivas como `node_modules` o entornos virtuales `.venv`, verificando que estÃ©n excluidos en `.gitignore` para evitar saturaciÃ³n de sincronizadores en la nube.

---

### Protocolo 5: Cierre de Turno / Handoff
1. **EjecuciÃ³n de Relevo Saliente:** Al finalizar una tarea o tanda de requerimientos, ejecutar `skills/ops-gestion-relevo/SKILL.md` en **MODO SALIDA**.
2. **SincronizaciÃ³n de Contexto:** Actualizar `.context/activeContext.md` y `.context/progress.md` reflejando con exactitud el estado final.
3. **Commit de Entrega:** Asegurar que todos los cambios queden respaldados en un commit atÃ³mico y descriptivo.