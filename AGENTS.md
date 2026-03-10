# Repository Guidelines

## Project Structure & Module Organization

This repository is organized as a single Python package inside `lerato/`. Core implementation lives in `lerato/src/lerato/`, split by language stage: `lexer.py`, `parser.py`, `transpiler.py`, `runtime.py`, `cli.py`, and supporting AST/error modules. Tests live in `lerato/tests/` and mirror those stages with files such as `test_lexer.py` and `test_runtime.py`. Example `.ler` programs for manual checks live in `lerato/examples/`. Planning and language notes are kept in `lerato/PROJECT_PLAN.md`, `lerato/DOCUMENTATION.md`, and `lerato/RUN_TEST_PLAN.md`.

## Build, Test, and Development Commands

Run commands from `lerato/`.

- `uv run --with pytest pytest` runs the full test suite.
- `uv run --with pytest pytest tests/test_parser.py` runs one test module while iterating.
- `uv run lerato --version` checks the CLI entrypoint.
- `uv run lerato examples/hello.ler` executes a sample Lerato program.
- `python -m pip install -e .[dev]` installs the package and `pytest` without `uv` if needed.

## Coding Style & Naming Conventions

Target Python 3.11+ and follow the existing style: 4-space indentation, type hints on public functions, and small focused modules. Use `snake_case` for functions, variables, and test names; use `PascalCase` for AST node and error classes such as `FunctionDefStmt` and `LeratoSyntaxError`. Keep user-facing Lerato keywords ASCII-only and aligned with the documented language forms in `DOCUMENTATION.md`. Prefer short docstrings only where the purpose is not obvious from the code.

## Testing Guidelines

Pytest is the test framework. Add or update tests with every language feature or bug fix, especially when changing parsing, runtime behavior, or error messages. Name files `test_<area>.py` and test functions `test_<behavior>()`. Cover both valid execution paths and failure cases with line-aware syntax/runtime errors where relevant.

## Commit & Pull Request Guidelines

Recent commits use short, imperative subjects like `Add bilingual syntax errors` and `Usage examples`. Follow that pattern: lead with the action, keep the subject specific, and avoid punctuation noise. Pull requests should include a brief description, the user-visible behavior change, linked issues if any, and sample `.ler` input or console output when CLI behavior changes.

## Security & Configuration Tips

Do not commit virtual environments, cache directories, or generated `__pycache__/` output. Keep examples and fixtures small, text-based, and safe to execute locally through the `lerato` CLI.
