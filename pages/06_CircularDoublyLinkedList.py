import streamlit as st

from core.algos.linear.circular_doubly_linked_list_ops import build_steps, parse_operations
from core.render.linear.circular_doubly_linked_list_graphviz import cdll_to_dot
from core.stepper import Stepper
from core.ui.sidebar import render_sidebar_nav

render_sidebar_nav("linear")

st.title("Circular Doubly Linked List — Visualizador")

default_ops = """# Ejemplo
push_back 1
push_back 2
push_back 3
rotate_left 1
push_front 9
find 2
pop_back
rotate_right 2
delete 9
delete_all 2
"""

ops_text = st.text_area("Operaciones:", value=default_ops, height=220)

if st.button("Construir pasos", type="primary"):
    try:
        ops = parse_operations(ops_text)
        steps = build_steps(ops, dot_builder=cdll_to_dot)
        st.session_state["cdll_stepper"] = Stepper(steps=steps, index=0)
    except ValueError as e:
        st.error(str(e))

stepper: Stepper | None = st.session_state.get("cdll_stepper")

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
    st.code(f"CDLL (desde head): {step.values}", language="python")
