import streamlit as st

from core.algos.stack_ops import build_steps, parse_operations
from core.render.stack_graphviz import stack_to_dot
from core.stepper import Stepper

st.title("Stack (Pila) — Visualizador")

default_ops = """# Ejemplo
push 10
push 7
push 3
pop
push 99
"""

colA, colB = st.columns([2, 1], gap="large")

with colA:
    ops_text = st.text_area("Operaciones (push/pop):", value=default_ops, height=180)
    if st.button("Construir pasos", type="primary"):
        try:
            ops = parse_operations(ops_text)
            steps = build_steps(ops, dot_builder=stack_to_dot)
            st.session_state["stack_stepper"] = Stepper(steps=steps, index=0)
        except ValueError as e:
            st.error(str(e))

    stepper: Stepper | None = st.session_state.get("stack_stepper")

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
        st.code(f"Stack: {step.stack}", language="python")

with colB:
    stepper = st.session_state.get("stack_stepper")
    if stepper is not None:
        step = stepper.current()
        st.graphviz_chart(step.dot, use_container_width=True, height=700)
    else:
        st.info("Aquí se mostrará el diagrama cuando construyas pasos.")
