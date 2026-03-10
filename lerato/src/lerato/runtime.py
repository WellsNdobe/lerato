"""Runtime helpers for executing Lerato programs."""

from __future__ import annotations

import difflib
from pathlib import Path
import traceback
from typing import Any

from lerato.errors import LeratoRuntimeError, LeratoSyntaxError
from lerato.transpiler import transpile_source

BUILTIN_NAMES = {
    "bontsha",
    "amogela",
    "tiro",
    "busa",
    "ge",
    "goba",
    "gefela",
    "gona",
    "tsenya",
    "feleletsa",
    "nnete",
    "maaka",
}


def transpile_for_execution(source: str) -> str:
    return transpile_source(source)


def execute_source(source: str, *, filename: str = "<memory>") -> dict[str, object]:
    globals_dict = _build_globals(Path(filename) if filename != "<memory>" else None)
    _execute_source(source, filename=filename, globals_dict=globals_dict)
    return globals_dict


def _build_globals(current_file: Path | None) -> dict[str, object]:
    globals_dict: dict[str, object] = {"__name__": "__main__", "amogela": input}
    globals_dict["__lerato_current_file__"] = current_file
    globals_dict["__lerato_loaded_files__"] = set()
    globals_dict["__lerato_import_stack__"] = []
    globals_dict["__lerato_import__"] = _make_importer(globals_dict)
    return globals_dict


def _make_importer(globals_dict: dict[str, object]):
    def _import_lerato(path_text: str) -> None:
        if not isinstance(path_text, str):
            raise LeratoRuntimeError(
                "import path must be a string.",
                sepedi_message="Tsela ya import e swanetše go ba sengwalwa.",
            )

        current_file = globals_dict.get("__lerato_current_file__")
        base_dir = Path(current_file).parent if isinstance(current_file, Path) else Path.cwd()
        import_path = (base_dir / path_text).resolve()
        if import_path.suffix != ".ler":
            raise LeratoRuntimeError(
                f"imported file must use the .ler extension: {path_text}",
                sepedi_message=f"Faele ya import e swanetše go fela ka .ler: {path_text}",
            )
        if not import_path.exists():
            raise LeratoRuntimeError(
                f"imported file not found: {import_path}",
                sepedi_message=f"Faele ye e tsentšwego ga e hwetšagale: {import_path}",
            )

        loaded_files = globals_dict["__lerato_loaded_files__"]
        if import_path in loaded_files:
            return

        import_stack = globals_dict["__lerato_import_stack__"]
        if import_path in import_stack:
            raise LeratoRuntimeError(
                f"circular import detected: {import_path}",
                sepedi_message=f"Go na le circular import: {import_path}",
            )

        previous_file = globals_dict.get("__lerato_current_file__")
        import_stack.append(import_path)
        try:
            source = import_path.read_text(encoding="utf-8")
            globals_dict["__lerato_current_file__"] = import_path
            _execute_source(source, filename=str(import_path), globals_dict=globals_dict)
            loaded_files.add(import_path)
        finally:
            import_stack.pop()
            globals_dict["__lerato_current_file__"] = previous_file

    return _import_lerato


def _execute_source(source: str, *, filename: str, globals_dict: dict[str, Any]) -> None:
    python_source = transpile_for_execution(source)

    try:
        exec(compile(python_source, filename, "exec"), globals_dict, globals_dict)
    except LeratoSyntaxError:
        raise
    except Exception as exc:
        raise _wrap_runtime_error(exc) from exc


def execute_file(path: str | Path) -> dict[str, object]:
    source_path = Path(path)
    source = source_path.read_text(encoding="utf-8")
    globals_dict = _build_globals(source_path.resolve())
    _execute_source(source, filename=str(source_path), globals_dict=globals_dict)
    return globals_dict


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
