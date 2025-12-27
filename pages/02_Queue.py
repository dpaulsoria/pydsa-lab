import streamlit as st

from core.algos.queue_ops import build_steps, parse_operations
from core.render.queue_graphviz import queue_to_dot
from core.stepper import Stepper

st.title("Queue (Cola) — Visualizador (FIFO)")

default_ops = """# Ejemplo FIFO
enqueue 8
enqueue 3
enqueue 2
dequeue
enqueue 1
"""

ops_text = st.text_area("Operaciones (enqueue/dequeue):", value=default_ops, height=180)

colA, colB = st.columns([1, 2], gap="large")

with colA:
    if st.button("Construir pasos", type="primary"):
        try:
            ops = parse_operations(ops_text)
            steps = build_steps(ops, dot_builder=queue_to_dot)
            st.session_state["queue_stepper"] = Stepper(steps=steps, index=0)
        except ValueError as e:
            st.error(str(e))

    stepper = st.session_state.get("queue_stepper")

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
        st.code(f"Queue: {step.queue}", language="python")

with colB:
    stepper = st.session_state.get("queue_stepper")
    if stepper is not None:
        step = stepper.current()
        st.graphviz_chart(step.dot, use_container_width=True)
    else:
        st.info("Aquí se mostrará el diagrama cuando construyas pasos.")
