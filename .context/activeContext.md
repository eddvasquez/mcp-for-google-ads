# Contexto activo

Agente Activo: Codex.

Implementación autorizada del plan de ejecutor recuperable para google-ads-palabras-clave-nuevas. Cambios finales en src/ads_mcp/extensions/changes.py (clasificación/reintentos preflight), tools/editing.py (contrato del cliente), tests/test_preflight_recovery.py y README_es.md. Código compartido por CLI y herramientas MCP, sin transporte adicional.

30 pruebas offline de edición y recuperación aprobadas. EXPIRED y PREFLIGHT_RETRYABLE prueban NOT_SENT; UNKNOWN/APPLYING/UNVERIFIED siguen sin reintento. Solo lecturas y validate_only transitorios admiten tres intentos. Mutación real se envía una sola vez. Aprobación por contenido en cliente diario: cambio de ID técnico no exige nuevo consentimiento si payload y condiciones autorizadas son idénticos y no hay incertidumbre. Cambio de contenido o fase de activación sí exige nueva aprobación.

Skill del Hub guardada en 335049a: motor SQLite fuera de repositorio, publish/resume/reconcile/import-legacy, 104 pruebas. Proyecto consumidor Ana Maria Tre migró en lectura 48 altas verificadas y seis pendientes, sin publicación ni activación. Informe del consumidor docs/mineria_palabras_clave/ejecutor_recuperable.md. No se cambiaron credenciales ni dependencias.

Siguiente paso ejecutable: para una publicación solicitada, usar la CLI mantenida del Hub y el journal execution_ del proyecto consumidor; no generar scripts de emergencia ni reintentar propuestas inciertas. Los procesos MCP que ya estaban ejecutándose necesitan reinicio para cargar el código nuevo; no se reiniciaron en este turno. Mantener separado el permiso de mantenimiento del de publicación o activación.