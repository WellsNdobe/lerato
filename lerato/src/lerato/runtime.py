"""Runtime helpers for executing Lerato programs."""

from __future__ import annotations

import difflib
from pathlib import Path
import traceback

from lerato.errors import LeratoRuntimeError, LeratoSyntaxError
from lerato.transpiler import transpile_source

BUILTIN_NAMES = {
    "bontsha",
    "tiro",
    "busa",
    "ge",
    "gona",
    "feleletsa",
    "nnete",
    "maaka",
}


def transpile_for_execution(source: str) -> str:
    return transpile_source(source)


def execute_source(source: str, *, filename: str = "<memory>") -> dict[str, object]:
    python_source = transpile_for_execution(source)
    globals_dict: dict[str, object] = {"__name__": "__main__"}

    try:
        exec(compile(python_source, filename, "exec"), globals_dict, globals_dict)
    except LeratoSyntaxError:
        raise
    except Exception as exc:
        raise _wrap_runtime_error(exc) from exc

    return globals_dict


def execute_file(path: str | Path) -> dict[str, object]:
    source_path = Path(path)
    source = source_path.read_text(encoding="utf-8")
    return execute_source(source, filename=str(source_path))


def _wrap_runtime_error(exc: Exception) -> LeratoRuntimeError:
    line = _extract_line_number(exc)

    if isinstance(exc, NameError):
        name = getattr(exc, "name", None)
        suggestion = _closest_name(name) if name else None
        if name and suggestion:
            return LeratoRuntimeError(
                f"name or command '{name}' is not defined. Did you mean '{suggestion}'?",
                sepedi_message=(
                    f"Leina goba taelo '{name}' ga e tsebje. Na o be o nyaka '{suggestion}'?"
                ),
                line=line,
            )
        if name:
            return LeratoRuntimeError(
                f"name or command '{name}' is not defined.",
                sepedi_message=f"Leina goba taelo '{name}' ga e tsebje.",
                line=line,
            )

    return LeratoRuntimeError(
        str(exc),
        sepedi_message=f"Lenaneo le paletswe ge le kitimisiwa: {exc}",
        line=line,
    )


def _extract_line_number(exc: Exception) -> int | None:
    tb = traceback.extract_tb(exc.__traceback__)
    if not tb:
        return None
    return tb[-1].lineno


def _closest_name(name: str) -> str | None:
    matches = difflib.get_close_matches(name, sorted(BUILTIN_NAMES), n=1, cutoff=0.6)
    if not matches:
        return None
    return matches[0]
