# PyDSA Lab — Chat Handoff (para continuar en otro chat)

## Contexto del proyecto
PyDSA Lab es un laboratorio de Estructuras de Datos y Algoritmos en Python con:
- UI: Streamlit (páginas en `pages/`)
- Visualización: Graphviz (renders en `core/render/*_graphviz.py`)
- Lógica de simulación: `core/algos/*_ops.py` (parse + handlers + build_steps)
- Estructuras: `core/structures/*/*.py`
- Navegación: `core/ui/sidebar.py`
- Tests: `tests/` con pytest + smoke tests + coverage

Objetivo: cada módulo permite ejecutar operaciones “paso a paso” (Prev/Next/Reset) y ver:
- diagrama (`dot`)
- estado en texto (listas/buckets/etc)

## Convenciones que estamos usando
### Separación por capas
- `core/structures/...`:
  - Implementación de la estructura (no depende de Streamlit/Graphviz).
  - Métodos “puros”: insert/delete/search/etc.
  - `snapshot()` retorna dict para UI/tests.
- `core/algos/.../*_ops.py`:
  - `parse_operations(text) -> list[Operation]`
  - `HANDLERS` (dict op_kind -> handler)
  - `build_steps(ops, ..., dot_builder=...) -> list[Step]`
  - Manejo de errores: captura IndexError/KeyError/OverflowError y corta simulación con mensaje.
- `core/render/.../*_graphviz.py`:
  - Funciones `*_to_dot(...) -> str`
  - Acepta parámetros highlight_* cuando aplica.
- `pages/*.py`:
  - Streamlit: inputs, botón “Construir pasos”, Stepper en session_state, graphviz_chart, texto.

### Sobre “OpKind”
Tendencia actual:
- Evitar enums dentro de `core/structures/*` si no aportan a la estructura.
- Mantener OpKind/handlers en `*_ops.py` (más fácil de refactorizar y testear).
- Los tests pueden fallar si renombramos campos de `Step` (ej: `queue` -> `values`), así que mantener consistencia.

### Tests
- “Smoke tests”: verifican que módulos cargan y que funciones `*_to_dot` devuelven un `str` válido.
- Tests funcionales: verifican operaciones básicas (`insert/delete/get/contains` etc).
- Evitar asumir que `items()` retorna list: puede ser generador (convertir con `list()` en tests).

## Estado actual (resumen)
- Lineales (00-08): OK con ops + render + pages + tests
- Hash (09-11): OK con ops + render + pages + tests (OJO: ordered_map_graphviz espera buckets de tuplas)
- Árboles:
  - 12 Binary Tree: OK
  - 13 BST: OK (insert/delete/height/is_valid_bst/traversals)
  - 14 AVL: (si ya está) o pendiente según branch
  - 15 Red-Black (LLRB): **pendiente / en progreso** (opción B = structure + ops)

## Próximo trabajo sugerido (checklist)
### Red-Black Tree (LLRB) — Opción B
1) `core/structures/trees/red_black_tree.py`
   - Nodo con color (RED/BLACK)
   - helpers: is_red, rotate_left, rotate_right, flip_colors
   - insert + delete (si decides implementar delete ahora o después)
   - invariantes: no-red-right, no-dos-rojos-seguidos, black-height consistente (validación)
   - snapshot (inorder + bfs + quizá lista de nodos con color)

2) `core/algos/trees/red_black_tree_ops.py`
   - parse_operations: insert/delete/contains/min/max/traversals
   - handlers y build_steps (con highlights si quieres)

3) `core/render/trees/red_black_tree_graphviz.py`
   - dibujar nodos con color (fillcolor rojo/negro)
   - edges left/right, opcional resaltado de camino

4) `pages/15_RedBlackTree.py`
   - UI similar a BST
   - st.number_input si requieres parámetros
   - Stepper en session_state

5) `tests/trees/`:
   - smoke: to_dot
   - estructura: invariantes básicas post-insert
   - ops: build_steps no rompe y snapshots coherentes

## Preguntas rápidas que el asistente debería hacerle a este repo
- ¿Dónde están ubicados los árboles? (`core/structures/trees/` vs `core/structures/`)
- ¿Cómo se llaman los campos estándar de Step en este proyecto? (normalmente `dot`, `message`, y estado `values/buckets/...`)
- ¿Qué firma usa `*_to_dot` del árbol para highlights?
