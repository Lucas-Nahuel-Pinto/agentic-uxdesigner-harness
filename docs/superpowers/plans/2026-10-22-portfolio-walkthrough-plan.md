# Plan de implementación: Walkthrough cinemático 3D del portfolio

- **Fecha**: 2026-10-22
- **Spec**: `docs/superpowers/specs/2026-10-22-portfolio-walkthrough-design.md` (aprobado)
- **Repo destino**: `C:\Agentic-Quality-Engineer\Projects\Lucas-Nahuel-Pinto.github.io`
- **Regla**: cada fase termina con algo ejecutable y verificable; no se avanza de fase con criterios de aceptación incumplidos.

---

## Fase 1 — Base: app cliente + menú (sin 3D)

**Objetivo**: la home es la app del walkthrough, con menú de videojuego funcional.

| # | Tarea | Detalle |
|---|---|---|
| 1.1 | Estructura de la app en Astro | Entrada `src/pages/es/index.astro` y `en/index.astro` como shell de la app; TS en `src/walkthrough/` |
| 1.2 | `StateMachine` | Estados `MENU → CUTSCENE → FP → PANEL → CASE`; API: `set(state)`, `on(state, cb)`; sin dependencias |
| 1.3 | Menú de videojuego | Idioma ES/EN, sonido ON/OFF, botón COMENZAR; persiste preferencias en `localStorage`; estética de título de videojuego |
| 1.4 | `i18n` JSON | `es.json` / `en.json`: menú, subtítulos del storyboard, textos de panel y viñetas; cambio en caliente |
| 1.5 | `AudioManager` | Reproduce SFX de menú y voces desde archivo (Audio API); `setLanguage()`, `setMuted()`; wire de subtítulos con timestamps del audio |
| 1.6 | Guard en COMENZAR | Estado "cargando intro" con spinner de estilo; habilita con ~5 s bufferizadas (dummy al principio) |

**Aceptación**: menú navega ES/EN con textos cambiando en caliente, sonido on/off persiste, COMENZAR dispara `CUTSCENE` (con placeholder de video). Playwright: smoke del menú en ambos idiomas.

## Fase 2 — Animatic: validar la cinemática antes de renderizar

**Objetivo**: escuchar y ver los 43 s con audio real y tiempos correctos, en HTML.

| # | Tarea | Detalle |
|---|---|---|
| 2.1 | Reproductor de animatic | Página interna (no pública) que reproduce el storyboard plano por plano con el audio `ElevenLabs_..._Johan Steve.mp3` |
| 2.2 | Timeline | Tiempos exactos por plano (los de la tabla del spec, ajustables); subtítulos sincronizados con el AudioManager ya escrito |
| 2.3 | SALTAR + loop | Probar el salto y el retome |
| 2.4 | Review con el usuario | Ajustar timings/dialogo antes de tocar Blender (barato de cambiar acá, caro después) |

**Aceptación**: usuario aprueba la secuencia con audio real; timeline aprobada = guion de animación de la Fase 3.

**Entregable audio EN**: usuario genera la voz EN en ElevenLabs (mismo estilo); se sube a `public/audio/`.

## Fase 3 — Blender: personajes, oficina y render del video

**Prerequisito**: instalar **blender-mcp** (agregar a `opencode.jsonc` + addon en Blender) → requiere reiniciar la sesión del agente.

**Pipeline (decidido 2026-10-23)**: Blender puro con assets stylized simples, sin etapa de video generativa IA — la IA video rompe sync por construcción, consistencia de personajes, control de cámara/match-cut y el reuso del set como GLB (spec decisión 11).

| # | Tarea | Detalle |
|---|---|---|
| 3.1 | Set de oficina | Mirror's Edge Catalyst: amplia, blanca, ventanales, minimalista; un solo set fuente para video Y GLB futuro |
| 3.2 | Personajes (4) | Fantasma (gel azul, sin boca, manos flotantes, **luz interior pulsante al hablar**), avatar Lucas, 🦊 zorro UX, 🐿️ ardilla dev — los tres con gafas de sol |
| 3.3 | Rigs + clips | Hablar, volar, posesión, sobresalto, pulgar; actuación del fantasma: vibración corporal por cadencia del audio, **luz interior sincronizada por envolvente de amplitud (ffmpeg → keyframes)**, manos expresivas, ojos/cejas |
| 3.4 | Doodles 2D | Planos billboard al lado del fantasma con keyframes alineados al audio (sync por construcción) |
| 3.5 | Cámara | Objeto animado: 7 planos del spec; **giro orbital 180°** con encuadre constante; zoom final a la nuca; **DOF: fondo desenfocado en planos 1–2** (atención en fantasma y doodles; EEVEE DOF nativo) |
| 3.6 | Render | EEVEE (Cycles opcional para posesión); salida WebM VP9 + MP4 H.264, 2 bitrates (desktop/móvil) + poster; ≤ 8 MB desktop |
| 3.7 | Audio separado | El video sale **sin audio embebido**; voces ES/EN como mp3 sueltos |

**Aceptación**: video con todos los planos, doodles sincronizados por construcción, peso dentro de presupuesto, aprobación del usuario.

## Fase 4 — Escena FP: three.js + HUD AR + grilla

| # | Tarea | Detalle |
|---|---|---|
| 4.1 | Integración de video | `VideoPlayer` real: buffer, SALTAR, error→FP, match-cut en la nuca |
| 4.2 | `ThreeScene` | Oficina exportada a GLB (Draco + KTX2), luces, cámara primera persona; manos y entorno; **sin gafas en cuadro** |
| 4.3 | Interacción | Raycast de mano con mouse (escritorio), táctil en móvil; hover/feedback de selección |
| 4.4 | HUD AR | Overlay HTML estilo HUD (translúcido, acentos de color, tipografía técnica) que arranca con la **grilla de 3 proyectos** (datos reales de los proyectos) |
| 4.5 | Calidad adaptativa | FPS < 45 por > 2 s → baja resolución, LOD, apaga bloom/sombras |
| 4.6 | Fallbacks | Sin WebGL → modo liviano low-poly → sitio HTML tradicional; video caído → FP directo |

**Aceptación**: recorrido menú → saltar → FP → grilla a 60 FPS en escritorio medio; ≥ 30 FPS en móvil; fallbacks probados.

## Fase 5 — Revista AR: viñetas + integración con case studies

| # | Tarea | Detalle |
|---|---|---|
| 5.1 | Visor de revista | Overlay con identidad propia (papel/cómic, separada del HUD); abre al tocar tarjeta |
| 5.2 | Viñetas por proyecto | 3 intros (origen de la idea + problema) en viñetas con **parallax de capas** (fondo/personaje/bocadillo/texto) e interactivas; contenido de las páginas de proyecto existentes |
| 5.3 | Navegación | "Ver caso completo" → Astro navega al case study; "volver" regresa al panel con estado guardado; botón de vuelta a la grilla |
| 5.4 | i18n de viñetas | Textos ES/EN en JSON |

**Aceptación**: los 3 proyectos se abren como revista, parallax fluido, ida y vuelta al case study sin perder estado, en ES y EN.

## Fase 6 — Pulido, pruebas y lanzamiento

| # | Tarea | Detalle |
|---|---|---|
| 6.1 | Suite Playwright | Flujo completo ES/EN, sonido on/off, saltar, fallbacks (sin WebGL, video fallido) |
| 6.2 | Performance real | Presupuestos del spec: menú < 1 s, video ≤ 8 MB, GLB ≤ 3 MB; Lighthouse en case studies (SEO) |
| 6.3 | Matriz de dispositivos | Desktop medio, gama baja, móvil táctil — medición de FPS con DevTools |
| 6.4 | Accesibilidad | Subtítulos visibles siempre, navegación por teclado en menú y HUD, contraste del HUD |
| 6.5 | Deploy | GitHub Pages (build Astro); verificar rutas `/es/`, `/en/`, `/es/proyectos/*` y sitemap |

**Aceptación**: todos los criterios de éxito del spec cumplidos; deploy verificado en producción.

---

## Dependencias externas (usuario)

1. **Audio EN en ElevenLabs** (fase 2) — voz estilo Johan Steve, misma frase traducida.
2. **blender-mcp instalado + Blender local** (fase 3) — lo configuro yo, reinicio de sesión después.
3. **Validaciones de animatic y render** (fases 2 y 3) — aprobación tuya en cada hito.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Render de Blender toma más de lo previsto | Animatic primero valida todo antes de renderizar; EEVEE mantiene iteraciones baratas |
| Peso del video en móvil | 2 bitrates; si aún pasa, recortar el plano 1 |
| Calidad de la voz EN de ElevenLabs | Se cambia el archivo sin tocar nada más (audio separado del video) |
| El HUD choca con la Revista AR | Identidades separadas ya definidas; probar transición en fase 5 temprano |
