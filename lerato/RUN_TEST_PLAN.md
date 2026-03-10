# Lerato Run/Test Plan

## Purpose

This document explains how to run and verify the current Lerato prototype.

## Current Status

As of March 10, 2026, the full version 0 prototype is working. You can:

- execute `.ler` programs end to end
- run the full pytest suite
- test the CLI entrypoint
- inspect the lexer, parser, transpiler, and runtime stages independently

## Recommended Commands

### Run Tests

```powershell
uv run --with pytest pytest
```

Without `uv`:

```powershell
python -m pytest
```

### Show Package Version

```powershell
uv run lerato --version
```

Without `uv`:

```powershell
python -m lerato.cli --version
```

### Run A Lerato Program

```powershell
uv run lerato examples/hello.ler
```

Without `uv`:

```powershell
python -m lerato.cli examples/hello.ler
```

Expected current behavior:

- the CLI executes `.ler` files
- syntax errors surface as Lerato syntax errors
- runtime failures are wrapped with Lerato runtime errors

## Minimum Demo Goal

This program should run successfully:

```lerato
bontsha("Dumela Lefase")
```

Function demo:

```lerato
tiro kopanya(a, b) gona
    busa a + b
feleletsa

bontsha(kopanya(2, 3))
```

Conditional demo:

```lerato
ge nnete gona
    bontsha("go lokile")
feleletsa
```

## Recommended Manual Checks

1. `uv run lerato --version`
2. `uv run --with pytest pytest tests/test_basic.py`
3. `uv run --with pytest pytest tests/test_lexer.py`
4. `uv run --with pytest pytest tests/test_parser.py`
5. `uv run --with pytest pytest tests/test_transpiler.py`
6. `uv run --with pytest pytest tests/test_runtime.py`
7. run all files in `examples/` through the CLI

## Verified Example Files

These example programs are expected to run successfully:

- `examples/hello.ler`
- `examples/variables.ler`
- `examples/arithmetic.ler`
- `examples/if_check.ler`
- `examples/nested_check.ler`
- `examples/function_add.ler`
