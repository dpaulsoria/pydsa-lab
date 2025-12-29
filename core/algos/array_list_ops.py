from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.structures.array_list import ArrayList, OpKind


@dataclass(frozen=True)
class Operation:
    kind: OpKind
    a: Any | None = None
    b: Any | None = None


@dataclass(frozen=True)
class Step:
    dot: str
    values: list[Any]
    message: str


def _parse_value(token: str) -> Any:
    try:
        return int(token)
    except ValueError:
        return token


def parse_operations(text: str) -> list[Operation]:
    ops: list[Operation] = []
    for i, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        cmd = parts[0].lower()

        try:
            if cmd == OpKind.APPEND:
                ops.append(Operation(OpKind.APPEND, _parse_value(parts[1])))
            elif cmd == OpKind.INSERT:
                ops.append(Operation(OpKind.INSERT, int(parts[1]), _parse_value(parts[2])))
            elif cmd == OpKind.POP:
                ops.append(Operation(OpKind.POP))
            elif cmd == OpKind.POP_AT:
                ops.append(Operation(OpKind.POP_AT, int(parts[1])))
            elif cmd == OpKind.REMOVE_FIRST:
                ops.append(Operation(OpKind.REMOVE_FIRST, _parse_value(parts[1])))
            elif cmd == OpKind.GET:
                ops.append(Operation(OpKind.GET, int(parts[1])))
            elif cmd == OpKind.SET:
                ops.append(Operation(OpKind.SET, int(parts[1]), _parse_value(parts[2])))
            elif cmd == OpKind.CLEAR:
                ops.append(Operation(OpKind.CLEAR))
            else:
                raise ValueError(
                    f"Línea {i}: comando no válido '{parts[0]}'. "
                    "Usa append/insert/pop/pop_at/remove/get/set/clear."
                )
        except IndexError as err:
            raise ValueError(f"Línea {i}: faltan argumentos para '{cmd}'.") from err
        except ValueError as err:
            raise ValueError(f"Línea {i}: argumentos inválidos para '{cmd}'.") from err

    return ops


def build_steps(ops: list[Operation], dot_builder: callable) -> list[Step]:
    arr: ArrayList[Any] = ArrayList()

    def snap(msg: str, hi: int | None = None) -> Step:
        vals = arr.to_list()
        return Step(dot=dot_builder(vals, highlight_index=hi), values=vals, message=msg)

    steps: list[Step] = [snap("Estado inicial")]

    for op in ops:
        try:
            if op.kind == OpKind.APPEND:
                arr.append(op.a)
                steps.append(snap(f"append {op.a}"))

            elif op.kind == OpKind.INSERT:
                idx = int(op.a)
                arr.insert(idx, op.b)
                steps.append(snap(f"insert {idx} {op.b}", hi=idx))

            elif op.kind == OpKind.POP:
                removed = arr.pop()
                steps.append(snap(f"pop → {removed}"))

            elif op.kind == OpKind.POP_AT:
                idx = int(op.a)
                removed = arr.pop_at(idx)
                steps.append(
                    snap(
                        f"pop_at {idx} → {removed}",
                        hi=min(idx, max(len(arr) - 1, 0)) if len(arr) else None,
                    )
                )

            elif op.kind == OpKind.REMOVE_FIRST:
                ok = arr.remove_first(op.a)
                steps.append(snap(f"remove {op.a} → {'OK' if ok else 'NO ENCONTRADO'}"))

            elif op.kind == OpKind.GET:
                idx = int(op.a)
                val = arr.get(idx)
                steps.append(snap(f"get {idx} → {val}", hi=idx))

            elif op.kind == OpKind.SET:
                idx = int(op.a)
                arr.set(idx, op.b)
                steps.append(snap(f"set {idx} {op.b}", hi=idx))

            else:  # clear
                arr.clear()
                steps.append(snap(OpKind.CLEAR))

        except (IndexError, ValueError) as e:
            steps.append(snap(f"ERROR: {e} (se detuvo la simulación)"))
            break

    return steps
