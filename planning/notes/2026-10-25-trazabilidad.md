# Análisis de trazabilidad — 2026-10-25

Notas de una sesión de análisis sobre por qué spectrace no logra del todo su objetivo
(evitar código huérfano/muerto y cosas sin registrar al mutar un proyecto) y qué
alternativas hay. **Nada de esto está decidido**: es material para retomar.

## Objetivo original

Rastrear cada cambio de decisión para que, al cambiarla, no quede código huérfano,
código muerto, funciones muertas ni cosas implementadas sin mencionar en agentes/skills.

## Estado actual (diagnóstico del usuario)

- **Funciona bien:** specs y `planning/` — detallan todo y guían a cualquier agente al goal.
  Los errores son más de usuario que del agente.
- **Funciona a medias:** el rastreo de cada función y su sincronía con spec y documentación.
- **Problema raíz:** al mutar el proyecto (añadir/modificar funciones) el agente
  olvida que algo ya existe, olvida borrar lo que ya no se usa, y olvida que algo
  afecta a otra cosa.

## Hallazgos técnicos sobre `.spectrace/`

| Archivo | Qué es | Problema |
|---|---|---|
| `changes/*.patch` (209, ~1.4 MB) | Diff de cada tarea | **Versionados** (corrección: no están ignorados). Duplican lo que ya está en los commits; crecen sin límite (`005-T009.patch` = 164 KB). |
| `changes/*.touch.json` (~50) | Símbolos por tarea (spec 012) | Versionados; otra copia del mismo dato. Tareas viejas usan `.patch`, nuevas `touch.json`, con modo "anchored" para conciliar. |
| `fingerprints.json` (~18 KB) | Hash del texto de cada R/D/A + `_ids` | Estado derivado **versionado y reescrito** (`model.py:419`, en `review` y `status --write`) → siempre aparece como `M`, conflictos de merge entre ramas. |
| `index.db` (~4.5 MB) | Grafo/caché de símbolos (spec 013) | Ignorado por git — **correcto**: es función del código y se regenera (`trace index --rebuild`, o en memoria en CI, 014/R6). |

Otros hallazgos:
- `leftover` (012/D6) solo marca símbolos que la tarea retirada *añadió* y cuyo cuerpo
  sigue *idéntico* por hash: basta tocar una línea para que se escape. No mira símbolos
  modificados, llamadores, config, docs ni tests.
- El código muerto que nunca pasó por una tarea es invisible: ninguna spec lo cubre.
- El registro depende de que el agente llame `start`/`done`; si no, queda "outside the trace".

### La raíz en las specs

- **001/R2@1:** cambios registrados "without a commit and without touching the staging area".
- **A9@1:** "Commits are optional for the trace".

Por eso spectrace reimplementa partes de git: snapshots (`refs/spectrace/*`), patches,
seguimiento de renames (`patches.py:follow`), `restore` con `git apply -R`, fingerprints.

### Pasado vs presente (dónde encaja el grafo)

| | Pasado (ledger) | Presente (grafo) |
|---|---|---|
| Pregunta | ¿Quién hizo esto y bajo qué decisión? | ¿Quién depende de esto hoy? |
| Comandos | `why`, `impact <decisión>`, `leftover`, `restore` | `impact <símbolo>`, `--deep`, `locate`, `packet` |
| Fuente de verdad | historial (debe compartirse) | el código actual (se recalcula) |

La unión entre ambos es la dirección de símbolo `path::Qualified.name` (012/D10).

## Alternativas discutidas

### A. Commit como ledger (reemplazo)
Una tarea = un commit con trailers (`Spec-Task`, `Covers`, `Retires`, `Kind`).
Elimina `.patch`, `touch.json` (se calcula de `commit^..commit`), `refs/spectrace`,
`fingerprints.json` (se responde con `git log -S "D3@2" -- planning/`).
- Riesgos: squash merge fusiona diffs; rompe 001/R2 y A9 (requiere `spectrace-change`);
  CI necesita `fetch-depth: 0`; migrar 209 tareas.
- **El usuario no quiere cambiar el motor a la ligera** — descartado por ahora.

### B. Todo con git, sin script
Git cubre el pasado en cualquier lenguaje: `log --grep`, `show`, `revert -n`,
`log --follow -M`, `blame`, `log -L :funcion:archivo`, `log -S`, `grep -w`, hook `commit-msg`.
Con `.gitattributes` (`diff=golang|rust|python`, regex `xfuncname` para TS y Dart)
git sabe a qué función pertenece cada hunk — lo que intenta la spec 019, en una línea.
- Git **no** da: grafo de dependencias, código muerto, validación de `planning/`.
- Código muerto mejor delegado a linters: `knip` (TS), `cargo`/`cargo-udeps` (Rust),
  `deadcode`/`staticcheck` (Go), `dart analyze` (Dart), `vulture` (Python).

### C. Complemento: `Symbols:` en cada commit (sin cambiar el motor)
```
Spec-Task: 002/T004
Covers: 002/D3@2
Symbols: src/store.ts::validateTitle (added), src/store.ts::addItem (modified)
```
- Pros: bajo riesgo (capa extra), cualquier lenguaje, viaja con git, legible sin
  herramientas, mejora la limpieza al retirar (`git log --grep "Covers: 002/D3"`),
  puede generarse en `done` desde los hunk headers.
- Contras: lo declarado puede no ser real (hay que verificar contra el diff); da
  tarea→función pero no función→función; los nombres envejecen con renames;
  precisión aproximada fuera de Python (solo avisar, no bloquear — A11);
  obliga a un commit por tarea; squash; duplicación con `touch.json` mientras convivan.
- Veredicto: mejor **como complemento**, si `done` lo genera y fuera de Python solo avisa.

## Reencuadre: el problema es de atención, no de registro

| Olvido | Momento | Pregunta no hecha | Fuente confiable |
|---|---|---|---|
| "Ya existe" | antes de crear | ¿hay algo que ya hace esto? | búsqueda de texto (`locate`, `git grep`) |
| "Afecta a aquello" | antes de modificar | ¿quién usa lo que cambio? | tests y compilador/linter (el grafo es pista) |
| "Olvidó borrar" | después de retirar | ¿qué quedó del enfoque viejo? | decisión→tareas→símbolos (valor único de spectrace) |
| **"No lo registró"** | después de crear | ¿dónde más debe aparecer esto? | **reglas de alineación** (ver abajo) |

Causas probables de que el agente olvide aunque haya datos:
1. No consulta (nada lo obliga en el momento justo).
2. Respuesta ruidosa o vacía engañosa (TS sin adaptador → "no dependents").
3. Ruido de fondo (`fingerprints.json` siempre modificado, cientos de patches)
   que enseña a ignorar `.spectrace/`.

Arreglos candidatos: (a) obligar consulta en los momentos clave (protocolo + `check`),
(b) mejorar calidad de respuesta ("no analizado" en vez de vacío), (c) limpiar ruido.

## Caso concreto: tools de MCP sin registrar

Se agregaron tools a un MCP y no se registraron en `AGENTS.md` ni en el skill.
Ninguna herramienta lo detecta: `locate` (era nuevo), `impact`/grafo (no hay arista
código→`AGENTS.md`), `leftover` (nada retirado), `covers:` (la tarea cumplió su decisión).

Es un **olvido de propagación**: crear algo genera obligaciones en otros lugares.
La relación es una **regla del proyecto**, no está en el código.

Este repo ya lo resolvió para sí mismo a mano en **020/R7** (`trace audit` marca
comandos de `cli.py` faltantes en "Tracing tools" y documentados que ya no existen).

### Propuesta: reglas de alineación declarativas por proyecto
```
- tools MCP:  definidas en src/**/*.ts por server.tool("<nombre>"
              deben aparecer en AGENTS.md, skills/*/SKILL.md
- endpoints:  definidos en api/** por @router.(get|post)("<ruta>"
              deben aparecer en docs/api.md
```
`check` extrae nombres por regex y reporta en ambos sentidos: falta registrar /
documentación menciona algo que ya no existe.
- Pros: cualquier lenguaje; exacto (puede bloquear sin violar A11); bidireccional;
  barato (020/R7 generalizado).
- Contras: hay que escribir reglas por proyecto (ideal: que start/plan las propongan);
  regex frágil si cambia la forma de declarar; verifica mención, no descripción correcta.
- Prevención: si una D agrega superficie expuesta (tool, comando, endpoint, evento),
  `spectrace-plan` genera la tarea de registrarla.

## Próximo paso pendiente

- Identificar el proyecto del caso MCP y cómo se declaran sus tools
  (`server.tool(...)`, decorador, archivo de registro) para escribir la regla concreta
  y comprobar que atrapa el caso real.
- Reunir 2–3 casos reales más de fallos (qué se cambió, qué se olvidó, lenguaje/repo)
  para decidir entre (a)/(b)/(c) antes de tocar specs o motor.
- Orden tentativo si se avanza: reglas de alineación → limpiar ruido de `.spectrace/`
  → 019 (adaptadores) → 020 (docs, al final para no documentar lo que cambiará).
