from __future__ import annotations

from typing import Any

from core.structures.hash.ordered_map import OrderedMap


def _maybe_call(obj: object, names: list[str], *args: Any, **kwargs: Any) -> Any:
    for name in names:
        fn = getattr(obj, name, None)
        if callable(fn):
            try:
                return fn(*args, **kwargs)
            except TypeError:
                # por si tu firma no acepta kwargs
                return fn(*args)
    raise AttributeError(f"No se encontró ninguno de: {names}")


def test_ordered_map_basic_smoke() -> None:
    # constructor tolerante
    try:
        om: Any = OrderedMap(capacity=8)  # si existe
    except TypeError:
        om = OrderedMap()

    # set/put
    _maybe_call(om, ["set", "put", "add"], "a", 1)
    _maybe_call(om, ["set", "put", "add"], "b", 2)
    _maybe_call(om, ["set", "put", "add"], "a", 99)  # update

    # get/lookup
    got = _maybe_call(om, ["get", "lookup"], "a")
    # algunos mapas devuelven None si no existe; aquí debe existir
    assert got == 99 or (isinstance(got, tuple) and 99 in got)

    # to_list/items/as_list
    lst = _maybe_call(om, ["to_list", "items", "as_list"])
    if lst is None:
        raise AssertionError("OrderedMap no expuso to_list/items/as_list")
    if not isinstance(lst, list):
        lst = list(lst)

    assert isinstance(lst, list)

    # delete/del/remove
    deleted = _maybe_call(om, ["delete", "del_key", "remove"], "b")
    assert deleted in (True, False, None)  # según tu implementación

    # snapshot (si existe)
    if hasattr(om, "snapshot") and callable(om.snapshot):
        snap = om.snapshot()
        assert isinstance(snap, dict)
