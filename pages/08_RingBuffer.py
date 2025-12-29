import streamlit as st

from core.algos.ring_buffer_ops import build_steps, parse_operations
from core.render.ring_buffer_graphviz import ring_buffer_to_dot
from core.stepper import Stepper
from core.ui.sidebar import render_sidebar_nav

render_sidebar_nav()
st.title("Ring Buffer — Visualizador (buffer circular)")

capacity = st.number_input("Capacidad", min_value=1, max_value=64, value=5, step=1)

default_ops = """# write = encola (sin overwrite)
# write_over = encola pisando si está lleno
write 10
write 20
write 30
read
write 40
peek
write_over 99
"""

ops_text = st.text_area("Operaciones:", value=default_ops, height=220)

if st.button("Construir pasos", type="primary"):
    try:
        ops = parse_operations(ops_text)
        steps = build_steps(ops, capacity=int(capacity), dot_builder=ring_buffer_to_dot)
        st.session_state["rb_stepper"] = Stepper(steps=steps, index=0)
    except ValueError as e:
        st.error(str(e))

stepper: Stepper | None = st.session_state.get("rb_stepper")

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
    st.code(
        f"items (orden lógico): {step.items}\n"
        f"buffer (slots): {step.buffer}\n"
        f"head={step.head} tail={step.tail} size={step.size}/{step.capacity}",
        language="python",
    )
