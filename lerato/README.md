# Lerato

Lerato is a beginner-friendly programming language prototype inspired by Sepedi. It uses a small handwritten pipeline in Python: lexer -> parser -> transpiler -> runtime.

## Current Status

Version `0.1.0` is a working single-file prototype. The repository currently supports:

- `bontsha(...)` output
- variable assignment
- numbers, strings, and booleans
- arithmetic and comparison expressions
- `ge ... gona ... feleletsa` conditionals
- `tiro ... gona ... busa ... feleletsa` functions
- execution of `.ler` files through the CLI

All example programs in `examples/` run successfully through the CLI.

## Install

### For development with `uv`

```powershell
uv run --with pytest pytest
uv run lerato --version
```

### Without `uv`

Install with standard Python tooling:

```powershell
python -m pip install -e .[dev]
python -m pytest
python -m lerato.cli --version
```

After publishing, end users should be able to install with `pip install lerato`.

## Run Lerato

Run a source file:

```powershell
uv run lerato examples/hello.ler
```

or without `uv`:

```powershell
python -m lerato.cli examples/hello.ler
```

## Example

```lerato
tiro kopanya(a, b) gona
    busa a + b
feleletsa

bontsha(kopanya(2, 3))
```

## Tests

Run the full test suite:

```powershell
uv run --with pytest pytest
```

Run a focused test file:

```powershell
uv run --with pytest pytest tests/test_parser.py
```

## Project Layout

- `src/lerato/` contains the implementation.
- `tests/` contains lexer, parser, transpiler, runtime, and basic CLI tests.
- `examples/` contains small runnable `.ler` programs.
- `DOCUMENTATION.md` is the language reference.
- `PROJECT_PLAN.md` tracks the prototype scope and milestones.
