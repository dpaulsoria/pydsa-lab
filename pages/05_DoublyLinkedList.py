import streamlit as st

from core.algos.doubly_linked_list_ops import build_steps, parse_operations
from core.render.doubly_linked_list_graphviz import doubly_linked_list_to_dot
from core.stepper import Stepper
from core.ui.sidebar import render_sidebar_nav

render_sidebar_nav()
st.title("Doubly Linked List — Visualizador")

default_ops = """# Ejemplo
push_back 1
push_back 2
push_back 3
find 2
delete 2
push_front 9
pop_back
reverse
"""

ops_text = st.text_area("Operaciones:", value=default_ops, height=200)

if st.button("Construir pasos", type="primary"):
    try:
        ops = parse_operations(ops_text)
        steps = build_steps(ops, dot_builder=doubly_linked_list_to_dot)
        st.session_state["dll_stepper"] = Stepper(steps=steps, index=0)
    except ValueError as e:
        st.error(str(e))

stepper: Stepper | None = st.session_state.get("dll_stepper")

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
    st.code(f"List: {step.values}", language="python")
