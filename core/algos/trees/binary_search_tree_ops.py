from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from core.structures.trees.binary_search_tree import BinarySearchTree


class OpKind(StrEnum):
    INSERT = "insert"
    DELETE = "delete"
    SEARCH = "search"
    INORDER = "inorder"
    PREORDER = "preorder"
    POSTORDER = "postorder"
    BFS = "bfs"
    CLEAR = "clear"


@dataclass(frozen=True)
class Operation:
    kind: OpKind
    value: Any | None = None


@dataclass(frozen=True)
class Step:
    dot: str
    values: list[Any]  # inorder (siempre)
    traversal: list[Any] | None
    message: str


def _parse_value(tok: str) -> Any:
    try:
        return int(tok)
    except ValueError:
        return tok


def parse_operations(text: str) -> list[Operation]:
    ops: list[Operation] = []
    for i, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        cmd = parts[0].lower()

        try:
            kind = OpKind(cmd)
        except ValueError as err:
            raise ValueError(
                f"Línea {i}: comando no válido '{parts[0]}'. "
                "Usa insert/delete/search/inorder/preorder/postorder/bfs/clear."
            ) from err

        if kind in {OpKind.INSERT, OpKind.DELETE, OpKind.SEARCH}:
            if len(parts) < 2:
                raise ValueError(f"Línea {i}: '{kind.value}' requiere un valor.")
            ops.append(Operation(kind=kind, value=_parse_value(parts[1])))
        else:
            ops.append(Operation(kind=kind))

    return ops


Handler = Callable[
    [BinarySearchTree[Any], Operation], tuple[str, list[Any] | None, list[Any] | None, Any | None]
]
# retorna: (message, highlight_values, traversal, highlight_target)


def _h_insert(
    t: BinarySearchTree[Any], op: Operation
) -> tuple[str, list[Any] | None, list[Any] | None, Any | None]:
    ok = t.insert(op.value)
    return (f"insert {op.value} → {'OK' if ok else 'YA EXISTE'}", None, None, None)


def _h_delete(
    t: BinarySearchTree[Any], op: Operation
) -> tuple[str, list[Any] | None, list[Any] | None, Any | None]:
    ok = t.delete(op.value)
    return (f"delete {op.value} → {'OK' if ok else 'NO ENCONTRADO'}", None, None, None)


def _h_search(
    t: BinarySearchTree[Any], op: Operation
) -> tuple[str, list[Any] | None, list[Any] | None, Any | None]:
    trace = t.search_trace(op.value)
    found = t.contains(op.value)
    return (f"search {op.value} → {found}", trace, None, op.value if found else None)


def _h_inorder(
    t: BinarySearchTree[Any], _op: Operation
) -> tuple[str, list[Any] | None, list[Any] | None, Any | None]:
    res = t.inorder()
    return (f"inorder → {res}", None, res, None)


def _h_preorder(
    t: BinarySearchTree[Any], _op: Operation
) -> tuple[str, list[Any] | None, list[Any] | None, Any | None]:
    res = t.preorder()
    return (f"preorder → {res}", None, res, None)


def _h_postorder(
    t: BinarySearchTree[Any], _op: Operation
) -> tuple[str, list[Any] | None, list[Any] | None, Any | None]:
    res = t.postorder()
    return (f"postorder → {res}", None, res, None)


def _h_bfs(
    t: BinarySearchTree[Any], _op: Operation
) -> tuple[str, list[Any] | None, list[Any] | None, Any | None]:
    res = t.bfs()
    return (f"bfs → {res}", None, res, None)


def _h_clear(
    t: BinarySearchTree[Any], _op: Operation
) -> tuple[str, list[Any] | None, list[Any] | None, Any | None]:
    t.clear()
    return ("clear", None, None, None)


HANDLERS: dict[OpKind, Handler] = {
    OpKind.INSERT: _h_insert,
    OpKind.DELETE: _h_delete,
    OpKind.SEARCH: _h_search,
    OpKind.INORDER: _h_inorder,
    OpKind.PREORDER: _h_preorder,
    OpKind.POSTORDER: _h_postorder,
    OpKind.BFS: _h_bfs,
    OpKind.CLEAR: _h_clear,
}


def build_steps(ops: list[Operation], dot_builder: callable) -> list[Step]:
    t: BinarySearchTree[Any] = BinarySearchTree()

    def snap(
        msg: str, hv: list[Any] | None = None, trav: list[Any] | None = None, ht: Any | None = None
    ) -> Step:
        inorder_vals = t.inorder()
        return Step(
            dot=dot_builder(t.root, highlight_values=hv, highlight_target=ht),
            values=inorder_vals,
            traversal=trav,
            message=msg,
        )

    steps: list[Step] = [snap("Estado inicial")]

    for op in ops:
        try:
            msg, hv, trav, ht = HANDLERS[op.kind](t, op)
            steps.append(snap(msg, hv=hv, trav=trav, ht=ht))
        except Exception as e:  # para no crashear la simulación
            steps.append(snap(f"ERROR: {e} (se detuvo la simulación)"))
            break

    return steps
