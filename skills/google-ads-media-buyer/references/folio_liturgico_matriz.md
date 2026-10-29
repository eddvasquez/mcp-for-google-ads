# Matriz de Mensajes Únicos, URLs Canónicas y Folio Litúrgico

Este documento define la matriz normativa de atribución silenciosa y coherencia semántica (*Message Match*) hacia WhatsApp para campañas de Google Ads de Respuesta Directa.

---

## 1. Ecuación Estructural del Enlace de WhatsApp

$$\mathbf{Mensaje\ Final} = \text{[Texto Base Semántico Específico]} + \text{ } + \mathbf{(Ref:\ [CAMP]-[PÁGINA]-[GCLID])}$$

- **CAMP:** Identificador de la campaña de origen (`R` = Retorno / dolor agudo, `H` = HighVolume, `T` = Tarot).
- **PÁGINA:** Nemónico de la intención / landing page (`ALT` = Altar/General, `AMT` = Alejar Amante, `BLQ` = Bloqueo en Redes, `VID` = Videncia/Psíquicos, `LMP` = Limpias, `FAC` = Facilidades/Pago por Resultados, `TRT` = Tarot).
- **GCLID:** Hash o identificador extraído del parámetro `gclid` de Google Ads persistido en `localStorage` o cookies por el Gestor Maestro de Atribución (`snippet_wordpress_whatsapp_master.html`).

---

## 2. Matriz Canónica de Derivación

| Campaña / Grupo | Slug / Intención | Mensaje Base Exclusivo (Continuación de Conversación Mental) | Folio Litúrgico | URL Destino Canónica (Google Ads) |
| :--- | :--- | :--- | :---: | :--- |
| **`Retorno` / General** | `/consulta-b/` | *«Hola, acabo de ver su página. Quisiera consultar mi caso de pareja en privado por favor.»* | `(Ref: R-ALT-[HASH])` | `https://tudominio.com/consulta-b/` |
| **`Retorno` / Consulta** | `/consulta-b/` | *«Hola, vi su página. Deseo consultar mi caso en el altar hoy para saber si mi situación tiene solución.»* | `(Ref: R-ALT-[HASH])` | `https://tudominio.com/consulta-b/` |
| **`Retorno` / Separación** | `/alejar-amt/` | *«Hola, vi su página sobre alejar malas influencias. Necesito una consulta privada sobre mi relación por favor.»* | `(Ref: R-AMT-[HASH])` | `https://tudominio.com/alejar-amt/` |
| **`Retorno` / Bloqueo** | `/consulta-b/` | *«Hola, vi su página. Me bloquearon de WhatsApp y quisiera una consulta en privado por favor.»* | `(Ref: R-BLQ-[HASH])` | `https://tudominio.com/consulta-b/` |
| **`Retorno` / Videncia** | `/vid-psiq/` | *«Hola, vi su página. Quisiera una consulta de videncia en privado para saber con sinceridad qué está pasando con mi pareja.»* | `(Ref: R-VID-[HASH])` | `https://tudominio.com/vid-psiq/` |
| **`Retorno` / Videncia Emerg.** | `/vid-psiq/` (Emerg.)| *«Hola, vi su página. Tengo un caso de EMERGENCIA con mi pareja y quisiera que revisen mi situación en privado por favor.»* | `(Ref: R-VID-[HASH])` | `https://tudominio.com/vid-psiq/` |
| **`Retorno` / Limpias** | `/limp-espir/` | *«Hola, vi su página sobre la limpia espiritual. Siento las cosas muy pesadas y quisiera una consulta en privado por favor.»* | `(Ref: R-LMP-[HASH])` | `https://tudominio.com/limp-espir/` |
| **`Retorno` / Limpia Emerg.**| `/limp-espir/` (Emerg.)| *«Hola, vi su página. Siento un daño y una pesadez muy fuerte, necesito una limpia de EMERGENCIA por favor.»* | `(Ref: R-LMP-[HASH])` | `https://tudominio.com/limp-espir/` |
| **`HighVolume` / Amarres** | `/consulta-b/` | *«Hola, vi su página sobre amarres de amor. Quisiera información para mi caso por favor.»* | `(Ref: H-AMR-[HASH])` | `https://tudominio.com/consulta-b/` |
| **`HighVolume` / Hechizos** | `/consulta-b/` | *«Hola, vi su página sobre rituales de amor. Quisiera saber cómo funciona por favor.»* | `(Ref: H-RIT-[HASH])` | `https://tudominio.com/consulta-b/` |
| **`HighVolume` / Facilidades**| `/facilidades-altar/` | *«Hola, vi su página y el compromiso de pagar solo por resultados. Quisiera consultar mi caso de pareja en privado por favor.»* | `(Ref: H-FAC-[HASH])` | `https://tudominio.com/facilidades-altar/` |
| **`Trt` / Tarot** | `/lectura-trt/` | *«Hola, buenas. Vi su página y quisiera una consulta de cartas para ver mi situación de pareja por favor.»* | `(Ref: T-TRT-[HASH])` | `https://tudominio.com/lectura-trt/` |

---

## 3. Directrices Inviolables de Destino Web

1. **Home (`/`) como Escudo Corporativo Sobrio (*Bland Corporate Shield*):**
   - La raíz institucional solo existe para revisión de bots de Google. Cero pauta publicitaria.
2. **Deprecación de Formularios Largos (`/consulta`):**
   - En tráfico móvil de urgencia emocional, formularios de 4 pasos provocan fugas de $>70\%$. El tráfico transaccional debe aterrizar siempre en la variante directa a WhatsApp (`/consulta-b/`).
3. **Auditoría Forense con el Cliente:**
   - Si el cliente o setter afirma no tener ventas de Google Ads, basta con revisar las capturas de chats entrantes: el texto exacto del mensaje o el folio `(Ref: ...)` delata irrefutablemente el origen pagado.
