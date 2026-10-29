# Lessons Learned & BitÃ¡cora de Correcciones

Este archivo registra decisiones rechazadas, errores identificados y correcciones permanentes del usuario para evitar reincidencias entre sesiones multi-agente.

## Formato de Entrada:
- **Fecha:** AAAA-MM-DD
- **Error/DesviaciÃ³n:** [DescripciÃ³n breve del enfoque incorrecto]
- **Regla Correctiva:** [InstrucciÃ³n innegociable para futuros turnos]
## 2026-10-29 — Recuperación diaria autorizada
- Error: tratar un fallo temporal de preflight como rechazo definitivo y exigir nueva aprobación por cambiar solo el ID técnico.
- Regla: preflight distingue EXPIRED y PREFLIGHT_RETRYABLE con prueba NOT_SENT; solo lecturas/validate_only temporales tienen tres intentos. La mutación real nunca se reintenta automáticamente. El cliente diario puede conservar consentimiento de contenido idéntico y fase idéntica, con equivalencia de payload y ausencia de resultado incierto.
- Verificación: 30 pruebas offline del backend aprobadas; Hub 335049a aporta ejecutor con estado SQLite y resume/reconcile. Sin mutaciones publicitarias durante este mantenimiento.
