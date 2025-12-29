import sys
from pathlib import Path

import streamlit as st

from core.ui.sidebar import render_sidebar_nav

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


st.set_page_config(page_title="PyDSA Lab", layout="wide")

render_sidebar_nav()  # <- LLAMADA

st.title("PyDSA Lab")
st.write("Selecciona un módulo en el menú lateral.")
