import streamlit as st


def render_sidebar_nav() -> None:
    with st.sidebar:
        st.title("PyDSA Lab")

        st.page_link("app.py", label="Inicio", icon="🏠")
        st.divider()

        with st.expander("Lineales", expanded=True):
            st.page_link("pages/01_Stack.py", label="Stack (LIFO)")
            st.page_link("pages/02_Queue.py", label="Queue (FIFO)")
            st.page_link("pages/03_LinkedList.py", label="Linked List")
            st.page_link("pages/04_Deque.py", label="Deque (Double Queue)")
            st.page_link("pages/05_DoublyLinkedList.py", label="Linked List (Doubly)")
            st.page_link("pages/07_SkipList.py", label="Skip List")
