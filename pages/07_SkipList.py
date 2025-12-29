import streamlit as st

from core.algos.linear.skip_list_ops import build_steps, parse_operations
from core.render.linear.skip_list_graphviz import skip_list_to_dot
from core.stepper import Stepper
from core.ui.sidebar import render_sidebar_nav

render_sidebar_nav("linear")

st.title("Skip List — Visualizer")

default_ops = """# Tip: para hacerlo determinista, usa insert VAL NIVEL
insert 10 2
insert 20 0
insert 30 1
search 20
delete 10
search 10
insert 25 2
"""

ops_text = st.text_area("Operaciones (insert/delete/search):", value=default_ops, height=220)

if st.button("Construir pasos", type="primary"):
    try:
        ops = parse_operations(ops_text)
        steps = build_steps(ops, dot_builder=skip_list_to_dot)
        st.session_state["skip_stepper"] = Stepper(steps=steps, index=0)
    except ValueError as e:
        st.error(str(e))

stepper: Stepper | None = st.session_state.get("skip_stepper")

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
    st.code("\n".join([f"L{i}: {row}" for i, row in enumerate(step.levels)]), language="text")
