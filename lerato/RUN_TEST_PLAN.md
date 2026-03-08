# Lerato Run/Test Plan

## Purpose

This document explains how to try Lerato at each stage of implementation, even before the full language pipeline is complete.

## Current Status

As of Day 2, the usable part of the project is the lexer. That means you can:

- install or run the package through `uv`
- run tests
- inspect whether Lerato source tokenizes correctly

You cannot yet execute `.ler` programs end to end. That becomes possible after the parser, transpiler, and runtime are wired together.

## Recommended Commands

### Run Tests

```powershell
uv run --with pytest pytest
```

### Show Package Version

```powershell
uv run lerato --version
```

### Current CLI Behavior

```powershell
uv run lerato examples/hello.ler
```

Expected current behavior:

- the CLI confirms the file path
- it does not yet execute Lerato code

## How To Try Features As They Become Usable

### Stage 1: CLI Bootstrap

What works:

- package install
- CLI startup
- version output

How to test:

```powershell
uv run lerato --version
```

### Stage 2: Lexer

What works:

- keyword recognition
- string and number tokenization
- operator tokenization
- line and column tracking

How to test:

```powershell
uv run --with pytest pytest tests/test_lexer.py
```

Suggested source snippets to validate through tests:

```lerato
bontsha("Dumela Lefase")
```

```lerato
x = 1 + 2
```

```lerato
ge nnete gona
feleletsa
```

### Stage 3: Parser

Target command once implemented:

```powershell
uv run --with pytest pytest tests/test_parser.py
```

What should be usable at that stage:

- valid `.ler` syntax parses into AST nodes
- invalid syntax reports useful line-based errors

### Stage 4: Transpiler

Target command once implemented:

```powershell
uv run --with pytest pytest tests/test_transpiler.py
```

What should be usable at that stage:

- Lerato source converts into Python source
- small examples can be inspected as generated Python

### Stage 5: Full Prototype

Target command once implemented:

```powershell
uv run lerato examples/hello.ler
```

What should be usable at that stage:

- `.ler` files execute end to end
- hello world, variables, arithmetic, `if`, and functions work

## Minimum Demo Goal

The first meaningful demo should be this program running successfully:

```lerato
bontsha("Dumela Lefase")
```

After that, the next demo should be:

```lerato
tiro kopanya(a, b) gona
    busa a + b
feleletsa

bontsha(kopanya(2, 3))
```

## Recommended Order For Manual Checks

1. `uv run lerato --version`
2. `uv run --with pytest pytest tests/test_basic.py`
3. `uv run --with pytest pytest tests/test_lexer.py`
4. later: parser tests
5. later: transpiler tests
6. finally: run example `.ler` files through the CLI
