import streamlit as st

from core.algos.linear.array_list_ops import build_steps, parse_operations
from core.render.linear.array_list_graphviz import array_list_to_dot
from core.stepper import Stepper
from core.ui.sidebar import render_sidebar_nav

render_sidebar_nav("linear")
st.title("Array / List — Visualizador (lista dinámica)")

default_ops = """# Ejemplo
append 10
append 20
insert 1 15
get 2
set 0 99
remove 15
pop
"""

ops_text = st.text_area("Operaciones:", value=default_ops, height=200)

if st.button("Construir pasos", type="primary"):
    try:
        ops = parse_operations(ops_text)
        steps = build_steps(ops, dot_builder=array_list_to_dot)
        st.session_state["array_stepper"] = Stepper(steps=steps, index=0)
    except ValueError as e:
        st.error(str(e))

stepper: Stepper | None = st.session_state.get("array_stepper")

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

    st.graphviz_chart(step.dot, use_container_width=True, height=260)
    st.write(f"**Acción:** {step.message}")
    st.code(f"ArrayList: {step.values}", language="python")
