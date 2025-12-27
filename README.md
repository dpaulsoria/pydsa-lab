# PyDSA Lab

PyDSA Lab es un laboratorio para practicar **Estructuras de Datos y Algoritmos** en Python, con un enfoque en **visualización** usando **Streamlit** y **Graphviz**.

La idea es que cada estructura/algoritmo se pueda ejecutar **paso a paso** (Prev/Next/Reset) y ver el estado tanto en **diagrama** como en **texto**.

---

## ✨ Objetivos

- Practicar DS/Algo de forma práctica (tipo entrevistas / retos).
- Ver el estado interno de cada solución de manera visual (no solo consola).
- Construir una base reutilizable para más visualizadores (sorting, linked list, trees, graphs, etc.).

---

## 🧱 Stack actual (MVP)

- ✅ Stack (Pila): `push`, `pop`, `peek`
- ✅ Generación de pasos (snapshots) para navegar la simulación
- ✅ Render con Graphviz (DOT)

---

## 📦 Requisitos

- Python **3.11+**
- **Graphviz** instalado en el sistema (necesario para `dot`)
  - Verificación:
    ```bash
    dot -V
    ```

> Si `dot -V` no funciona, instala Graphviz y asegúrate de que esté en el **PATH**.

---

## 🚀 Instalación

### Opción A — Instalación simple (recomendada para empezar rápido)

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate

pip install -U pip
pip install streamlit graphviz pydantic python-dotenv rich
pip install ruff mypy pytest pytest-cov pre-commit
```

### Opción B — Editable con extras dev (si ya tienes empaquetado configurado)
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

## 🧭 Cómo usar el visualizador de Stack

En la página **Stack (Pila)** escribe operaciones como:

```txt
# Ejemplo
push 10
push 7
push A
pop
push 99
```

- `push X` apila un valor
- `pop` desapila el último
- `#` comenta líneas

Después:
- **Construir pasos** → genera la simulación
- **Prev / Next / Reset** → navega el estado

---

## ✅ Calidad “pro” (lint, format, types, tests)

Ejecuta en este orden:

```bash
ruff check . --fix
ruff format .
mypy core
pytest
```

### Pre-commit (recomendado)

```bash
pre-commit install
pre-commit run --all-files
```

---

## 🗂️ Estructura del proyecto

```txt
PyDSA Lab/
├─ app.py
├─ pyproject.toml
├─ README.md
├─ pages/
│  └─ 01_Stack.py
├─ core/
│  ├─ __init__.py
│  ├─ stepper.py
│  ├─ algos/
│  │  ├─ __init__.py
│  │  └─ stack_ops.py
│  ├─ structures/
│  │  ├─ __init__.py
│  │  └─ stack.py
│  └─ render/
│     ├─ __init__.py
│     └─ stack_graphviz.py
└─ tests/
   └─ test_smoke.py
```

---

## 🛣️ Roadmap (próximos módulos)

- Sorting Visualizer (Bubble/Insertion/Selection → barras animadas)
- Linked List (nodos + flechas)
- Hash Table (buckets y colisiones)
- Trees (BST / Heap)
- Graphs (BFS/DFS/Dijkstra)

---

## 🧩 Ideas de mejora

- Modo Play/Pause con velocidad
- Historial de operaciones / log visual
- Exportar el diagrama (SVG/PNG)
- Editor de escenarios (guardar/cargar JSON)

---

## 📄 Licencia

MIT
