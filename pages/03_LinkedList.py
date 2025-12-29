import streamlit as st

from core.algos.linked_list_ops import build_steps, parse_operations
from core.stepper import Stepper
from core.ui.sidebar import render_sidebar_nav

render_sidebar_nav()

st.title("LInked List - Visualizer")

default_ops = """# Ejemplo
push_front 2
push_front 3
append 9
find 2
delete 3
find 3
"""

ops_text = st.text_area("Operaciones:", value=default_ops, height=180)

if st.button("Construir pasos", type="primary"):
    try:
        ops = parse_operations(ops_text)
        steps = build_steps(ops)
        st.session_state["ll_stepper"] = Stepper(steps=steps, index=0)
    except ValueError as e:
        st.error(str(e))

stepper = st.session_state.get("ll_stepper")

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

    step = stepper.current()
    st.graphviz_chart(step.dot, width="stretch", height="stretch")
    st.write(f"**Acción:** {step.message}")
    st.code(f"List: {step.values}", language="python")
