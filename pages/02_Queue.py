import streamlit as st

from core.algos.queue_ops import build_steps, parse_operations
from core.render.queue_graphviz import queue_to_dot
from core.stepper import Stepper
from core.ui.sidebar import render_sidebar_nav

render_sidebar_nav()

st.title("Queue (Cola) — Visualizador (FIFO)")

default_ops = """# Ejemplo FIFO
enqueue 8
enqueue 3
enqueue 2
dequeue
enqueue 1
"""

ops_text = st.text_area("Operaciones (enqueue/dequeue):", value=default_ops, height=180)

# 1) construir pasos
if st.button("Construir pasos", type="primary"):
    try:
        ops = parse_operations(ops_text)
        steps = build_steps(ops, dot_builder=queue_to_dot)
        st.session_state["queue_stepper"] = Stepper(steps=steps, index=0)
    except ValueError as e:
        st.error(str(e))

stepper: Stepper | None = st.session_state.get("queue_stepper")

# 2) navegación
if stepper is None:
    st.warning("Pulsa **Construir pasos** para generar la simulación.")
    st.info("Aquí se mostrará el diagrama cuando construyas pasos.")
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

    # 3) diagrama
    st.graphviz_chart(step.dot, use_container_width=True, width="stretch", height="stretch")

    # 4) estado
    st.write(f"**Acción:** {step.message}")
    st.code(f"Queue: {step.queue}", language="python")
