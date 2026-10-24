# Diseño: Walkthrough cinemático 3D para el portfolio de Lucas Pinto

- **Fecha**: 2026-10-22
- **Estado**: aprobado en brainstorming, pendiente de revisión del usuario sobre este documento
- **Repo destino**: `C:\Agentic-Quality-Engineer\Projects\Lucas-Nahuel-Pinto.github.io` (Astro 7)
- **Repo de trabajo (artefactos)**: `agentic-uxdesigner-harness` (`.superpowers/brainstorm/9857-1792691862/`)

## 1. Contexto y objetivo

Rediseño total del portfolio: el sitio actual **se reemplaza** por un walkthrough cinematográfico inspirado en videojuegos. El visitante entra a una oficina corporativa estilo *Mirror's Edge Catalyst*, es recibido por un fantasma que lo invita; el fantasma se lanza y **posee al avatar de Lucas** (no al revés: el cuerpo se sobresalta y el fantasma queda mandando adentro), y el visitante toma su lugar — termina explorando los tres proyectos en primera persona con un panel de realidad aumentada. En el POV **no se ven las gafas de sol**: el panel simplemente se enciende como si el usuario las llevara puestas.

**Prioridad**: balance 50/50 entre efecto wow cinemático y rapidez para reclutadores — el botón **SALTAR** siempre visible y carga de assets bajo demanda.

**Criterios de éxito**
- Recorrido completo menú → proyecto seleccionado sin trabas, en ES y EN.
- Ningún visitante queda en pantalla muerta (fallbacks verificados).
- Case studies HTML siguen indexables (SEO no se rompe).
- Funciona en móvil con 3D simplificado.

## 2. Decisiones tomadas

| # | Decisión | Alternativa descartada |
|---|---|---|
| 1 | Arquitectura **híbrida**: cinemática pre-render (Blender) + escena FP en three.js | 100% tiempo real (riesgo de performance/calidad); 100% pre-render (sin interacción) |
| 2 | Reemplaza el sitio actual; case studies Astro se conservan como rutas | Ruta aparte; proyecto separado |
| 3 | Móvil: 3D simplificado (mismo flujo, assets livianos, táctil) | Experiencia completa en móvil; fallback estático |
| 4 | Audio de voz **fuera del video** (AudioManager) → idioma/silencio en caliente | Audio embebido en el video |
| 5 | Fantasma **sin boca**: vibración corporal + movimiento expresivo + **manos flotantes** + **dibujos 2D** renderizados en Blender | Lip-sync (problemático); lenguaje de señas animado (descartado por el usuario) |
| 6 | Dibujos 2D **dentro del render de Blender** → imposible descincronización | Sprites en overlay HTML/CSS (riesgo de sync) |
| 7 | HUD de gafas (técnico, Mirror's Edge) ≠ Revista AR cómica (al abrir proyecto) — dos identidades separadas | Estilo cómic literal desde la grilla |
| 8 | Voz EN la genera el usuario en ElevenLabs (mismo estilo que la ES) | TTS del navegador; subtítulos sin voz EN |
| 9 | Los tres humanos/criaturas llevan **gafas de sol = dispositivo AR**; en el POV **no se muestran las gafas** — solo se enciende el HUD | Gafas visibles en primera persona; gafas solo en el panel |
| 10 | **Luz interior del fantasma** (emisión en el gel) que pulsa con la envolvente del audio mientras habla — indica visualmente de dónde sale la voz; misma animación sirve para ES y EN | Boca con visemas sincronizados (2 audios × 1 video → el otro idioma queda desincronizado) |
| 11 | Pipeline de video: **Blender puro**, assets stylized simples, EEVEE — iteración barata y el set se reutiliza como GLB en Fase 4 | Bloqueo en Blender "pasado por" modelo de video IA (drift de personajes, sin control de timing ni trayectoria de cámara, rompe sync por construcción y el match-cut) |

## 3. Flujo de escenas

```
Escena 1  Menú (HTML/CSS)         idioma ES/EN · sonido ON/OFF · COMENZAR
   ↓
Escena 2  Cinemática (video)      Blender → WebM/MP4 · SALTAR siempre
   ↓  (match-cut en la nuca)
Escena 3  Primera persona (three.js)  panel AR abierto con grilla de 3 proyectos
   ↓  selección con mano/ratón/táctil
Escena 4  Revista AR (overlay)    viñetas cómicas con parallax → "Ver caso completo"
   ↓
Escena 5  Case study HTML (Astro) /es/proyectos/*  → "volver" regresa al panel con estado
```

**Reglas de error y degradación**
- Video falla o no carga en 10 s → salto directo a Escena 3.
- Sin WebGL o GPU débil → modo liviano (low-poly, sin efectos); si falla → sitio HTML tradicional.
- Cambio de idioma en el menú aplica a audio, subtítulos y textos en caliente; dentro de la escena el idioma queda fijo hasta volver al menú.
- SONIDO OFF → silencia voces/SFX; subtítulos siguen visibles.
- Video cortado a mitad → retoma del buffer o salta a FP.

## 4. Storyboard — Escena 2 (~43 s, 7 planos, sin cortes duros)

| Plano | Tiempo | Contenido |
|---|---|---|
| 1 | 0:00–0:03 | Negros → oficina vacía, luz de ventana (establecimiento) |
| 2 | 0:03–0:23 | Primer plano del fantasma hablando: audio ES/EN + subtítulos + doodles 2D al lado |
| 3 | 0:23–0:27 | "Vení, acompañame" → vuelo al avatar central con estela luminosa |
| 4 | 0:27–0:31 | Posesión: destello → sobresalto → recuperación → pulgar; cámara acerca a la cara (con gafas) |
| 5 | 0:31–0:34 | Cartel HUD sutil "LUCAS PINTO — QA ENGINEER"; 🐿️ izquierda, avatar+gafas centro, 🦊 derecha |
| 6 | 0:34–0:40 | **Giro orbital de 180°** rodeando al personaje sin soltarlo del encuadre, termina detrás |
| 7 | 0:40–0:43 | Zoom a la nuca → match-cut → POV primera persona con panel AR encendiéndose |

**Equipo** (vista del usuario): 🐿️ ardilla-dev a la izquierda, avatar de Lucas al centro, 🦊 zorro-UX a la derecha. Los tres con gafas de sol.

**Actuación del fantasma**: sin boca; **luz interior pulsando con la envolvente del audio mientras habla** (el espectador ve de dónde sale la voz); ondas de vibración corporal con la cadencia del audio, cuerpo vivo, ojos/cejas expresivos, **dos manos flotantes separadas del cuerpo** como voz principal (gesticulan, apuntan, hacen "vení", se disuelven al poseer), y **dibujos 2D simples** que poppean al lado con el sentido de cada frase ("soy Lucas" → credencial, "portfolio" → mini-navegador, "herramientas" → lupa, "vení" → flecha).

## 5. Escenas 3 y 4 — primera persona y panel AR

- **Escena 3** (three.js): vista en los zapatos de Lucas; se ven manos + entorno (las gafas de sol **no aparecen en el cuadro**). El **HUD AR** —generado por las gafas que el personaje lleva puestas, fuera de pantalla— abre directo con la **grilla de los 3 proyectos**:
  1. QA Flow Checklists — 221 decisiones · 5 checklists
  2. Jira Traceability Manager — 2-3h → 30s
  3. Harness Manager — 6 pestañas de panorama
- **Estilo HUD**: tarjetas translúcidas con acentos de color, tipografía técnica, líneas finas — coherente Mirror's Edge. Selección con mano (raycast), ratón o táctil.
- **Escena 4 — Revista AR**: identidad distinta al HUD (revista digital leída en AR). Viñetas cómicas con parallax (capas: fondo, personaje, bocadillo, texto) e interactivas, con la intro del proyecto: cómo surgió la idea + qué problema resuelve. Botón "Ver caso completo" → Escena 5; botón de vuelta a la grilla.

## 6. Arquitectura técnica

**Capa 1 — Astro 7**: rutas `/es/` y `/en/` (home = app del walkthrough), `/es/proyectos/*` intactas, sitemap/SEO en páginas de proyecto.

**Capa 2 — App cliente (TypeScript, sin framework pesado)**
- `StateMachine` — dueño único del estado `MENU → CUTSCENE → FP → PANEL → CASE`; todo lo demás se suscribe.
- `VideoPlayer` — buffer, SALTAR, error → salta a FP.
- `AudioManager` — voz ES/EN fuera del video, SFX menú, ON/OFF global, sync de subtítulos.
- `ThreeScene` — oficina GLB, manos, gafas, raycast, calidad adaptable.
- `ARPanel` (overlay HTML) — grilla → viñetas → caso completo.
- `i18n (JSON es/en)` — menú, subtítulos, panel y viñetas; cambio en caliente.

**Capa 3 — Assets (`public/`)**: `intro.webm` + `intro.mp4` + poster · `oficina.glb` (Draco) · `manos.glb` · voces ES/EN mp3 · sprites de viñetas.

## 7. Pipeline de assets (Blender)

- **Blender + MCP** (blender-mcp) para trabajo repetitivo por script: camera path del giro 180°, parámetros de render, export batch; modelado a mano donde conviene.
- **Render**: EEVEE (Cycles como opción para el plano de la posesión).
- **Personajes (4)**: fantasma (gel azul, sin boca, manos flotantes), avatar de Lucas, zorro UX (pelaje realista con hair particles), ardilla dev (igual). Pelo corto del avatar con cards.
- **Entorno**: oficina Mirror's Edge Catalyst en Blender — un solo set que sirve para el render del video Y como fuente del GLB de la escena FP (versión simplificada) → coherencia visual total.
- **Animación**: rig de los 4 + clips (hablar, volar, posesión, sobresalto, pulgar); cámara como objeto animado; doodles 2D como planos billboard en la misma escena.
- **Export**:

| Salida | Uso |
|---|---|
| WebM (VP9) + MP4 (H.264), 2 bitrates + poster | video intro |
| GLB (Draco + KTX2) | oficina, manos, gafas para three.js |
| mp3/m4a ES y EN | voces del fantasma (EN: ElevenLabs, usuario) |
| PNG de viñetas | revista AR |

- **Límites**: video ≤ 8 MB · GLB ≤ 3 MB · texturas ≤ 2K.

## 8. Performance

- Menú < 1 s (HTML puro, cero assets 3D).
- COMENZAR habilitado con ~5 s de video bufferizadas; descarga en paralelo.
- 60 FPS escritorio gama media; ≥ 30 FPS móvil. Calidad adaptativa: si FPS < 45 por > 2 s → baja escala de resolución, LOD, desactiva bloom/sombras.
- Móvil: video bitrate bajo, low-poly, táctil en vez de mano.

## 9. Pruebas

- `playwright-cli`: flujo completo automatizado (menú → saltar → panel → viñeta → caso → volver), en ES y EN, sonido on/off.
- Degradación: sin WebGL, video fallido, GPU débil → siempre hay salida a FP o HTML.
- Lighthouse en case studies (SEO).
- Matriz de dispositivos reales + FPS con DevTools.
- Sync de subtítulos con audio (único punto de fallo posible; los doodles van en el render).

## 10. Plan de construcción (6 fases)

1. **Base**: Astro + StateMachine + menú de videojuego + i18n + AudioManager (sin 3D).
2. **Animatic**: storyboard en HTML con audio y tiempos → validar la cinemática antes de renderizar.
3. **Blender**: oficina + 4 personajes + rigs + actuación + render del video con doodles.
4. **Escena FP**: three.js con GLB + HUD AR + grilla de 3 proyectos.
5. **Revista AR**: viñetas con parallax + "Ver caso completo" + integración con case studies Astro.
6. **Pulido**: calidad adaptativa, fallbacks, pruebas, Lighthouse, accesibilidad.

## 11. Fuera de alcance

- Música/ambiente (posible con ACE-Step después).
- Zorro y ardilla en la escena FP (solo aparecen en el video).
- Lenguaje de señas animado (descartado).
- Case studies nuevos (se reutilizan los existentes).
