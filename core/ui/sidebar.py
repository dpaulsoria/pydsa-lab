from typing import Literal

import streamlit as st

Group = Literal["linear", "hash"]


def render_sidebar_nav(active_group: Group | None = None) -> None:
    # Persistimos el último grupo visitado (sin UI extra)
    if active_group is not None:
        st.session_state["nav_group"] = active_group

    group: Group = st.session_state.get("nav_group", "linear")

    with st.sidebar:
        st.title("PyDSA Lab")
        st.page_link("app.py", label="Home", icon="🏠")
        st.divider()

        with st.expander("Linear", expanded=(group == "linear")):
            st.page_link("pages/00_ArrayList.py", label="Array / List")
            st.page_link("pages/01_Stack.py", label="Stack (LIFO)")
            st.page_link("pages/02_Queue.py", label="Queue (FIFO)")
            st.page_link("pages/03_LinkedList.py", label="Linked List")
            st.page_link("pages/04_Deque.py", label="Deque (Double Queue)")
            st.page_link("pages/05_DoublyLinkedList.py", label="Linked List (Doubly)")
            st.page_link(
                "pages/06_CircularDoublyLinkedList.py", label="Circular Doubly Linked List"
            )
            st.page_link("pages/07_SkipList.py", label="Skip List")
            st.page_link("pages/08_RingBuffer.py", label="Ring Buffer")

        with st.expander("Hash", expanded=(group == "hash")):
            st.page_link("pages/09_HashTable.py", label="Hash Table / Map")
