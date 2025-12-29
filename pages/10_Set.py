import streamlit as st

from core.algos.hash.hash_set_ops import build_steps, parse_operations
from core.render.hash.hash_set_graphviz import hash_set_to_dot
from core.stepper import Stepper
from core.ui.sidebar import render_sidebar_nav

render_sidebar_nav("hash")
st.title("Set (HashSet) — Visualizador")

capacity = st.number_input(
    "Buckets (capacidad inicial)", min_value=4, max_value=64, value=8, step=1
)

default_ops = """# Ejemplo
add a
add b
add a
contains a
remove b
contains b
"""
ops_text = st.text_area("Operaciones:", value=default_ops, height=200)

if st.button("Construir pasos", type="primary"):
    try:
        ops = parse_operations(ops_text)
        steps = build_steps(ops, capacity=int(capacity), dot_builder=hash_set_to_dot)
        st.session_state["set_stepper"] = Stepper(steps=steps, index=0)
    except ValueError as e:
        st.error(str(e))

stepper: Stepper | None = st.session_state.get("set_stepper")

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
    st.code(f"Set: {step.values}", language="python")

if stepper is not None:
    step = stepper.current()
    st.graphviz_chart(step.dot, width="stretch", height="stretch")
else:
    st.info("Aquí se mostrará el diagrama cuando construyas pasos.")
