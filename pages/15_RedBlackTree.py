import streamlit as st

from core.algos.trees.red_black_tree_ops import build_steps, parse_operations
from core.render.trees.red_black_tree_graphviz import red_black_tree_to_dot
from core.stepper import Stepper
from core.ui.sidebar import render_sidebar_nav

render_sidebar_nav("trees")
st.title("Red-Black Tree (LLRB) — Visualizer")

default_ops = """# Inserciones típicas que fuerzan rotaciones/flip-colors
insert 10
insert 20
insert 30
insert 15
insert 25
insert 5
trace 25
contains 100
min
max
delete 20
bfs
"""

colA, colB = st.columns(2, gap="large")

with colA:
    ops_text = st.text_area("Operaciones:", value=default_ops, height=230)

    if st.button("Construir pasos", type="primary"):
        try:
            ops = parse_operations(ops_text)
            steps = build_steps(ops, dot_builder=red_black_tree_to_dot)
            st.session_state["rb_stepper"] = Stepper(steps=steps, index=0)
        except ValueError as e:
            st.error(str(e))

    stepper: Stepper | None = st.session_state.get("rb_stepper")

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
        st.code(
            f"inorder: {step.inorder}\n" f"bfs: {step.bfs}\n" f"height: {step.height}",
            language="python",
        )

with colB:
    stepper: Stepper | None = st.session_state.get("rb_stepper")

    if stepper is None:
        st.info("Aquí se mostrará el diagrama cuando construyas pasos.")
    else:
        st.graphviz_chart(step.dot, width="stretch", height="stretch")
