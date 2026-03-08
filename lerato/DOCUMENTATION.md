# Lerato Language Documentation

## Purpose

This document is the running language reference for Lerato.

It should be updated every time a new language feature becomes usable. The goal is to document real behavior that exists in the implementation, not planned features.

## Current Status

Lerato currently supports:

- `bontsha(...)` for output
- variable assignment with `=`
- numbers, strings, and booleans
- arithmetic and comparison expressions
- `ge ... gona ... feleletsa` if blocks
- `tiro ... gona ... feleletsa` function definitions
- `busa` return statements
- execution of `.ler` files through the CLI

## Running Lerato

Run a Lerato file:

```powershell
uv run lerato examples/hello.ler
```

Run the test suite:

```powershell
uv run --with pytest pytest
```

Show the CLI version:

```powershell
uv run lerato --version
```

## Language Basics

### File Extension

Lerato source files use the `.ler` extension.

### Blocks

Lerato uses explicit block markers:

- `gona` starts a block
- `feleletsa` ends a block

Indentation is allowed for readability, but `feleletsa` is what actually closes a block.

### Booleans

Lerato boolean values are:

- `nnete` for true
- `maaka` for false

## Built-in Output

### `bontsha(...)`

`bontsha` prints a value to the console.

Example:

```lerato
bontsha("Dumela Lefase")
```

Output:

```text
Dumela Lefase
```

Notes:

- `bontsha` is currently the main built-in function for visible output.
- It maps directly to Python `print(...)` in the current implementation.
- The function name must be spelled exactly as `bontsha`.

Common mistake:

```lerato
bontsh("Dumela")
```

This is invalid because `bontsh` is not a built-in Lerato function. The runtime now reports this as a bilingual Sepedi/English error and suggests `bontsha`.

## Variables

Variables are created with standard assignment syntax.

Example:

```lerato
leina = "Lerato"
palo = 10

bontsha(leina)
bontsha(palo)
```

Notes:

- A variable name uses identifier syntax such as `leina`, `palo`, or `karabo`.
- Variables do not need to be declared before assignment.

## Expressions

Lerato currently supports:

- numbers
- strings
- booleans
- identifiers
- function calls
- grouping with parentheses
- unary minus
- arithmetic operators
- comparison operators
- equality operators

### Arithmetic

Supported arithmetic operators:

- `+`
- `-`
- `*`
- `/`

Example:

```lerato
a = 8
b = 4
sephetho = a * b + 2

bontsha(sephetho)
```

### Comparisons

Supported comparison and equality operators:

- `>`
- `>=`
- `<`
- `<=`
- `==`
- `!=`

Example:

```lerato
ge 10 > 5 gona
    bontsha("10 is greater than 5")
feleletsa
```

## Conditionals

### `ge ... gona ... feleletsa`

Use `ge` to run code only when a condition is true.

Example:

```lerato
palo = 7

ge palo > 5 gona
    bontsha("Palo e feta 5")
feleletsa
```

Notes:

- `gona` must appear after the condition.
- `feleletsa` must close the block.
- `else` is not supported yet.

## Functions

### `tiro`

Use `tiro` to define a function.

Example:

```lerato
tiro kopanya(a, b) gona
    busa a + b
feleletsa
```

### `busa`

Use `busa` inside a function to return a value.

Example:

```lerato
tiro kopanya(a, b) gona
    busa a + b
feleletsa

karabo = kopanya(2, 3)
bontsha(karabo)
```

Notes:

- Parameters are written inside parentheses.
- Arguments are separated with commas.
- A function block must end with `feleletsa`.

## Minimal Syntax Reference

```lerato
bontsha("text")
name = expression

ge condition gona
    ...
feleletsa

tiro name(param1, param2) gona
    busa expression
feleletsa
```

## Current Limitations

Lerato does not support these yet:

- loops
- `else`
- imports
- classes
- modules
- collections as a formal language feature
- a REPL

## Documentation Update Rule

When a new Lerato feature becomes usable:

1. add a new section to this file
2. include at least one valid example
3. describe any syntax rules and limitations
4. update the "Current Status" section

This file should describe the language as it exists today, not as it might exist later.
