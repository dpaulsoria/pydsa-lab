from __future__ import annotations

import streamlit as st

from core.algos.trees.binary_search_tree_ops import build_steps, parse_operations
from core.render.trees.binary_search_tree_graphviz import binary_search_tree_to_dot
from core.stepper import Stepper
from core.ui.sidebar import render_sidebar_nav

render_sidebar_nav("trees")
st.title("Binary Search Tree (BST) — Visualizador")

default_ops = """# Inserta
insert 4
insert 2
insert 6
insert 1
insert 3
insert 5
insert 7

# Búsqueda (resalta camino)
search 5

# Recorridos
inorder
bfs

# Delete
delete 2
bfs
"""


colA, colB = st.columns(2, gap="large")

with colA:
    ops_text = st.text_area("Operaciones:", value=default_ops, height=260)

    if st.button("Construir pasos", type="primary"):
        try:
            ops = parse_operations(ops_text)
            steps = build_steps(ops, dot_builder=binary_search_tree_to_dot)
            st.session_state["bst_stepper"] = Stepper(steps=steps, index=0)
        except ValueError as e:
            st.error(str(e))

    stepper: Stepper | None = st.session_state.get("bst_stepper")

    if stepper is None:
        st.warning("Pulsa **Construir pasos** para generar la simulación.")
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Prev", disabled=not stepper.can_prev()):
                stepper.prev()
        with c2:
            if st.button("Reset"):
                stepper.reset()
        with c3:
            if st.button("Next", disabled=not stepper.can_next()):
                stepper.next()

        st.caption(f"Paso {stepper.index + 1} / {len(stepper.steps)}")
        step = stepper.current()

        st.write(f"**Acción:** {step.message}")
        st.code(f"Inorder (ordenado): {step.values}", language="python")
        if step.traversal is not None:
            st.code(f"Traversal: {step.traversal}", language="python")

with colB:
    stepper: Stepper | None = st.session_state.get("bst_stepper")

    if stepper is not None:
        st.graphviz_chart(step.dot, width="stretch", height="stretch")
    else:
        st.info("Aquí se mostrará el diagrama cuando construyas pasos.")
