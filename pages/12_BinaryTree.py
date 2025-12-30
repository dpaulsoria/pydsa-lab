import streamlit as st

from core.algos.trees.binary_tree_ops import build_steps, parse_operations
from core.render.trees.binary_tree_graphviz import binary_tree_to_dot
from core.stepper import Stepper
from core.ui.sidebar import render_sidebar_nav

render_sidebar_nav("trees")
st.title("Binary Tree — Visualizador")

default_ops = """# Ejemplo
insert 10
insert 20
insert 30
insert 40
find 30
traverse inorder
delete 20
traverse level
"""

ops_text = st.text_area("Operaciones:", value=default_ops, height=220)

if st.button("Construir pasos", type="primary"):
    try:
        ops = parse_operations(ops_text)
        steps = build_steps(ops, dot_builder=binary_tree_to_dot)
        st.session_state["bt_stepper"] = Stepper(steps=steps, index=0)
    except ValueError as e:
        st.error(str(e))

stepper: Stepper | None = st.session_state.get("bt_stepper")

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

    st.graphviz_chart(step.dot, width="stretch", height="stretch")
    st.write(f"**Acción:** {step.message}")
    st.code(f"Level-order: {step.values}", language="python")
    st.code(f"Levels: {step.levels}", language="python")
