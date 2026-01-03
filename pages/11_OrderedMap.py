import streamlit as st

from core.algos.hash.ordered_map_ops import build_steps, parse_operations
from core.render.hash.ordered_map_graphviz import ordered_map_to_dot
from core.stepper import Stepper
from core.ui.sidebar import render_sidebar_nav

render_sidebar_nav("hash")
st.title("Ordered Map — Visualizer (insertion-ordered)")

capacity = st.number_input(
    "Buckets (capacidad inicial)", min_value=4, max_value=64, value=8, step=1
)

default_ops = """# set key value
set a 10
set b 20
set c 30
set a 99
del b
get a
"""

colA, colB = st.columns([1, 1], gap="large")

with colA:
    ops_text = st.text_area("Operaciones:", value=default_ops, height=200)

    if st.button("Construir pasos", type="primary"):
        try:
            ops = parse_operations(ops_text)
            steps = build_steps(ops, capacity=int(capacity), dot_builder=ordered_map_to_dot)
            st.session_state["omap_stepper"] = Stepper(steps=steps, index=0)
        except ValueError as e:
            st.error(str(e))

    stepper: Stepper | None = st.session_state.get("omap_stepper")

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
        st.code(f"Ordered: {step.ordered}", language="python")

with colB:
    stepper: Stepper | None = st.session_state.get("omap_stepper")
    if stepper is not None:
        step = stepper.current()
        st.graphviz_chart(step.dot, width="stretch", height="stretch")
    else:
        st.info("Aquí se mostrará el diagrama cuando construyas pasos.")
