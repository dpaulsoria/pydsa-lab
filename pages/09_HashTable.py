import streamlit as st

from core.algos.hash.hash_table_ops import build_steps, parse_operations
from core.render.hash.hash_table_graphviz import hash_table_to_dot
from core.stepper import Stepper
from core.ui.sidebar import render_sidebar_nav

render_sidebar_nav("hash")
st.title("Hash Table / Dictionary / Map — Visualizador")

capacity = st.number_input(
    "Buckets (capacidad inicial)", min_value=4, max_value=64, value=8, step=1
)

default_ops = """# set key value
set a 10
set b 20
set a 99
get a
has c
delete b
"""

colA, colB = st.columns([2, 1], gap="large")

with colA:
    ops_text = st.text_area("Operaciones:", value=default_ops, height=200)

    if st.button("Construir pasos", type="primary"):
        try:
            ops = parse_operations(ops_text)
            steps = build_steps(ops, capacity=int(capacity), dot_builder=hash_table_to_dot)
            st.session_state["ht_stepper"] = Stepper(steps=steps, index=0)
        except ValueError as e:
            st.error(str(e))

    # 🔑 volver a leer después del botón
    stepper: Stepper | None = st.session_state.get("ht_stepper")

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
        st.write(f"**Acción:** {stepper.current().message}")
        st.code(f"Buckets: {stepper.current().buckets}", language="python")

with colB:
    stepper: Stepper | None = st.session_state.get("ht_stepper")
    if stepper is not None:
        step = stepper.current()
        st.graphviz_chart(step.dot, width="stretch", height="stretch")
    else:
        st.info("Aquí se mostrará el diagrama cuando construyas pasos.")
