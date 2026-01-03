# PyDSA Lab

PyDSA Lab es un laboratorio para practicar **Estructuras de Datos y Algoritmos** en Python con un enfoque en **visualización** usando **Streamlit** y **Graphviz**.

Cada módulo permite ejecutar operaciones **paso a paso** (Prev/Next/Reset) y ver el estado tanto en **diagrama** como en **texto**.

---

## ✨ Objetivos

- Practicar DS/Algo de forma práctica (tipo entrevistas / retos).
- Ver el estado interno de cada estructura de manera visual (no solo consola).
- Mantener una base reutilizable para agregar nuevos visualizadores (sorting, árboles, grafos, etc.).

---

## 🧱 Módulos actuales

**Lineales**
- ✅ **00 — Array / List** (lista dinámica): `append`, `insert`, `get`, `set`, `remove`, `pop`, `pop_at`, `clear`
- ✅ **01 — Stack (LIFO)**: `push`, `pop`, `peek`
- ✅ **02 — Queue (FIFO)**: `enqueue`, `dequeue`, `front` *(o `peek`, según implementación)*, `clear`
- ✅ **03 — Deque**: `push_front`, `push_back`, `pop_front`, `pop_back`, `peek_front`, `peek_back`, `clear`
- ✅ **04 — Singly Linked List**: `push_front`, `append`, `delete`, `delete_all`, `delete_at`, `search`, `find`, `find_index`, `reverse`, `to_list`
- ✅ **05 — Doubly Linked List**: `push_front`, `push_back`, `pop_front`, `pop_back`, `delete`, `delete_all`, `delete_at`, `find_index`, `reverse`, `to_list`, `to_reverse_list`
- ✅ **06 — Circular Doubly Linked List**: `push_front`, `push_back`, `pop_front`, `pop_back`, `delete`, `delete_all`, `find_index`, `rotate_left`, `rotate_right`, `to_list`, `to_reverse_list`
- ✅ **07 — Skip List**: `insert`, `delete`, `search`, `search_trace`, `levels_as_lists` *(resaltado del recorrido)*
- ✅ **08 — Ring Buffer**: `write`, `read`, `peek`, `clear`, `write_over`, `snapshot`

**Asociativos / Hash**
- ✅ **09 — Hash Table / Map**: `set`, `get`, `has`, `delete`, `snapshot`, `items`
- ✅ **10 — Set (conjunto)**: `add`, `remove`, `contains`, `to_list`, `snapshot`
- ✅ **11 — Ordered Map / Ordered Set**: `set`, `get`, `has`, `delete`, `items` *(en algunos casos `items()` es generador)*

**Arboles**
- ✅ **12 — Binary Tree**: `insert`, `delete`, `find/contains`, `inorder`, `preorder`, `postorder`, `bfs`, `clear`, `height`, `snapshot`
- ✅ **13 — Binary Search Tree (BST)**: `insert`, `delete`, `contains`, `min_value`, `max_value`, `inorder`, `preorder`, `postorder`, `bfs`, `height`, `is_valid_bst`, `search_trace`, `snapshot`
- ✅ **14 — AVL Tree (Balanceado)**: `insert`, `delete`, `contains`, `min_value`, `max_value`, `rotations` *(interno)*, `height`, `is_valid_avl`, `inorder/preorder/postorder/bfs`, `search_trace`, `snapshot`
- ✅ **15 — Red-Black Tree (LLRB)**: `insert`, `delete`, `contains`, `min_value`, `max_value`, `rotations/flip_colors` *(interno)*, `is_valid_llrb`, `inorder/preorder/postorder/bfs`, `search_trace`, `snapshot`

> Los nombres exactos de comandos dependen del archivo `core/structures/*_ops.py` de cada página.

## 🛣️ Roadmap: Módulos futuros
**Arboles**
- **16 — Heap (min-heap/max-heap)**
- **17 — Trie (prefijos)**
- **18 — Segment Trie**
- **19 — Fenwick Tree / BIT**
- **20 — B-Tree / B+Tree**

**Colas de Prioridad**
- **21 — Priority Queue**
- **22 — Heap**
- **23 — Fibonacci Heap**
- **24 — Binomial Heap**

**Estructuras Especiales**
- **25 — Union-Find / Disjoint Set (DSU)**
- **26 — LRU Cache (cash + doubly linked list)**
- **27 — Bloom Filter (probabilística)**
- **28 — Bitset / Bitmap**
- **29 — Sparse Matrix (matriz dispersa)**

**Persistentes / Inmutables (CS)**
- **30 — Persistent list / Tree**
- **31 — Rope (strings grandes)**
- **32 — Hash Array Mapped Trie (HAMT)**

**Concurrentes (Advanced)**
- **33 — Lock-free queue/stack**
- **34 — Concurrent hash map**
---

## 📦 Requisitos

- Python **3.11+**
- **Graphviz** instalado en el sistema (necesario para el binario `dot`)
  - Verificación:
    ```bash
    dot -V
    ```

Si `dot -V` no funciona, instala Graphviz y asegúrate de que esté en el **PATH**.

---

## 🚀 Instalación

### Opción A — Instalación simple (rápida)

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate

pip install -U pip
pip install -U streamlit graphviz pydantic python-dotenv rich

# Dev tools
pip install -U ruff mypy pytest pytest-cov pre-commit
```

### Opción B — Editable con extras dev

```bash
pip install -U pip setuptools wheel
pip install -e ".[dev]"
```

---

## ▶️ Ejecutar la app

```bash
streamlit run app.py
```

Luego abre el navegador en la URL que te muestre Streamlit.

---

## 🧭 Cómo usar los visualizadores (formato de operaciones)

En cada página, escribe una operación por línea. Puedes comentar con `#`.

Ejemplo (Stack):
```txt
push 10
push 7
peek
pop
push 99
```

Ejemplo (Array/List):
```txt
append 10
append 20
insert 1 15
get 2
set 0 99
remove 15
pop
```

Flujo:
- **Construir pasos** → genera la simulación (snapshots)
- **Prev / Next / Reset** → navega el estado
- El diagrama se renderiza con `st.graphviz_chart(...)`

---

## ✅ Calidad “pro” (lint, format, types, tests)

```bash
ruff check . --fix
ruff format .
mypy core
pytest -q
```

### Pre-commit (recomendado)

```bash
pre-commit install
pre-commit run --all-files
```

> Si un hook “modifica archivos”, vuelve a ejecutar:
> `git add .` y luego `git commit ...`

---

## 🗂️ Estructura del proyecto

```txt
PyDSA Lab/
├─ app.py
├─ pyproject.toml
├─ README.md
├─ pages/
│  ├─ 00_ArrayList.py
│  ├─ 01_Stack.py
│  ├─ 02_Queue.py
│  ├─ 03_Deque.py
│  ├─ 04_LinkedList.py
│  ├─ 05_DoublyLinkedList.py
│  ├─ 06_CircularDoublyLinkedList.py
│  └─ 07_SkipList.py
├─ core/
│  ├─ __init__.py
│  ├─ stepper.py
│  ├─ ui/
│  │  ├─ __init__.py
│  │  └─ sidebar.py
│  ├─ algos/
│  │  ├─ __init__.py
│  │  └─ *_ops.py
│  ├─ structures/
│  │  ├─ __init__.py
│  │  └─ *.py
│  └─ render/
│     ├─ __init__.py
│     └─ *_graphviz.py
└─ tests/
   └─ test_*.py
```

---

## 🧩 Ideas de mejora

- Modo Play/Pause con velocidad
- Historial de operaciones (log)
- Exportar diagrama (SVG/PNG)
- Guardar/cargar escenarios (JSON)
- Unificar parsing/dispatch con Enum + handlers (menos strings y más refactor-friendly)

---

## 📄 Licencia

SPDX-License-Identifier: MIT
