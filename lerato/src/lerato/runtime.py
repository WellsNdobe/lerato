"""Runtime helpers for executing Lerato programs."""

from __future__ import annotations

from pathlib import Path

from lerato.errors import LeratoRuntimeError, LeratoSyntaxError
from lerato.transpiler import transpile_source


def transpile_for_execution(source: str) -> str:
    return transpile_source(source)


def execute_source(source: str, *, filename: str = "<memory>") -> dict[str, object]:
    python_source = transpile_for_execution(source)
    globals_dict: dict[str, object] = {"__name__": "__main__"}

    try:
        exec(compile(python_source, filename, "exec"), globals_dict, globals_dict)
    except LeratoSyntaxError:
        raise
    except Exception as exc:  # pragma: no cover - exact Python errors vary by runtime path
        raise LeratoRuntimeError(str(exc)) from exc

    return globals_dict


def execute_file(path: str | Path) -> dict[str, object]:
    source_path = Path(path)
    source = source_path.read_text(encoding="utf-8")
    return execute_source(source, filename=str(source_path))
