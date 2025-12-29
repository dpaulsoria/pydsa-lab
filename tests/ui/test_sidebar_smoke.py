from __future__ import annotations

import importlib
import sys
from typing import Any


class _Ctx:
    def __enter__(self) -> _Ctx:
        return self

    def __exit__(self, *_exc: Any) -> bool:
        return False


class _FakeStreamlit:
    def __init__(self) -> None:
        self.sidebar = _Ctx()
        self.session_state: dict[str, object] = {}

    def title(self, *_a: Any, **_k: Any) -> None:
        return None

    def page_link(self, *_a: Any, **_k: Any) -> None:
        return None

    def divider(self, *_a: Any, **_k: Any) -> None:
        return None

    def expander(self, *_a: Any, **_k: Any) -> _Ctx:
        return _Ctx()


def test_sidebar_render_smoke(monkeypatch: Any) -> None:
    fake = _FakeStreamlit()
    monkeypatch.setitem(sys.modules, "streamlit", fake)

    import core.ui.sidebar as sidebar

    importlib.reload(sidebar)

    # tu función a veces acepta un arg (active_group) y a veces no.
    try:
        sidebar.render_sidebar_nav("hash")
    except TypeError:
        sidebar.render_sidebar_nav()
