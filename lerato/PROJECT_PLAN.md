# Lerato Project Plan

## 1. Project Overview

Lerato is a beginner-friendly programming language inspired by Sepedi and designed to be easy to type on standard keyboards. Version 0 should be a small Python implementation that can run simple `.ler` programs through a handwritten lexer, parser, and transpiler to Python.

The immediate goal is not a full compiler. The immediate goal is a working prototype that supports:

- `bontsha("Dumela Lefase")`
- variable assignment
- arithmetic
- `ge ... gona ... feleletsa`
- `tiro ... gona ... busa ... feleletsa`

This project exists to make early programming syntax feel more familiar to Sepedi speakers while keeping the implementation practical and teachable.

## 2. Implementation Principles

- Use Sepedi-inspired ASCII keywords only.
- Prefer one clear syntax form per feature.
- Keep blocks explicit with `gona` and `feleletsa`.
- Make version 0 single-file only.
- Prefer the fastest path to running valid `.ler` files.
- Reject unsupported syntax instead of guessing.

## 3. Version 0 Scope

### In Scope

- print/output
- string, number, and boolean literals
- variable assignment
- arithmetic and comparison expressions
- `if` blocks
- function definitions
- return statements
- command-line execution of a `.ler` file

### Out of Scope

- loops
- imports and modules
- classes
- collections beyond what is strictly needed
- static typing
- REPL
- package management
- optimization work

## 4. Keyword Mapping Table

| Lerato | Meaning | Example | Python Mapping |
| --- | --- | --- | --- |
| `bontsha` | print/show | `bontsha("Dumela")` | `print(...)` |
| `tiro` | function definition | `tiro kopanya(a, b) gona` | `def kopanya(a, b):` |
| `busa` | return | `busa a + b` | `return a + b` |
| `ge` | if | `ge x > 0 gona` | `if x > 0:` |
| `gona` | start block | `ge x > 0 gona` | `:` |
| `feleletsa` | end block | `feleletsa` | end indentation level |
| `nnete` | true | `ge nnete gona` | `True` |
| `maaka` | false | `ge maaka gona` | `False` |

## 5. Minimal Viable Grammar for Version 0

This grammar is intentionally narrow. It is enough to build the first working prototype.

```ebnf
program         := statement*

statement       := print_stmt
                 | assign_stmt
                 | if_stmt
                 | function_stmt
                 | return_stmt
                 | expr_stmt

print_stmt      := "bontsha" "(" expression ")" newline*
assign_stmt     := IDENTIFIER "=" expression newline*
if_stmt         := "ge" expression "gona" newline* statement* "feleletsa" newline*
function_stmt   := "tiro" IDENTIFIER "(" parameters? ")" "gona" newline* statement* "feleletsa" newline*
return_stmt     := "busa" expression newline*
expr_stmt       := expression newline*

parameters      := IDENTIFIER ("," IDENTIFIER)*
arguments       := expression ("," expression)*

expression      := equality
equality        := comparison (("==" | "!=") comparison)*
comparison      := term ((">" | ">=" | "<" | "<=") term)*
term            := factor (("+" | "-") factor)*
factor          := unary (("*" | "/") unary)*
unary           := ("-" unary) | primary
primary         := NUMBER
                 | STRING
                 | "nnete"
                 | "maaka"
                 | IDENTIFIER
                 | IDENTIFIER "(" arguments? ")"
                 | "(" expression ")"
```

### Grammar Notes

- Newlines should be tokenized because they help separate statements.
- Indentation in `.ler` source is optional for readability and should not affect parsing.
- `feleletsa` is the only block terminator in version 0.
- `else` should not be added yet.

## 6. Technical Architecture

### Execution Model

Use a transpile-and-run pipeline:

1. read `.ler` source
2. tokenize it
3. parse into an AST
4. transpile AST to Python source
5. execute the generated Python

This is the fastest route to a usable prototype and gives a simple debug path when behavior is wrong.

### Recommended Modules

| File | Responsibility |
| --- | --- |
| `src/lerato/lexer.py` | tokenization and source positions |
| `src/lerato/parser.py` | AST construction and syntax errors |
| `src/lerato/transpiler.py` | AST to Python generation |
| `src/lerato/runtime.py` | execution helpers and safe `exec` context |
| `src/lerato/cli.py` | file loading and command-line entry point |
| `src/lerato/ast_nodes.py` | AST dataclasses |
| `src/lerato/errors.py` | shared error classes |

### Parser Recommendation

Use a handwritten recursive-descent parser. The grammar is small enough that a parser library would slow down early iteration more than it helps.

## 7. Recommended Project Tree

```text
lerato/
├── PROJECT_PLAN.md
├── README.md
├── pyproject.toml
├── examples/
│   ├── hello.ler
│   ├── variables.ler
│   ├── arithmetic.ler
│   ├── if_check.ler
│   └── function_add.ler
├── src/
│   └── lerato/
│       ├── __init__.py
│       ├── ast_nodes.py
│       ├── cli.py
│       ├── errors.py
│       ├── lexer.py
│       ├── parser.py
│       ├── runtime.py
│       └── transpiler.py
└── tests/
    ├── test_basic.py
    ├── test_lexer.py
    ├── test_parser.py
    ├── test_runtime.py
    └── test_transpiler.py
```

### Structure Notes

- Keep all implementation code under `src/lerato`.
- Put only tiny runnable samples in `examples/`.
- Keep tests split by stage: lexer, parser, transpiler, runtime.
- Add no extra folders until the basic pipeline works.

## 8. Example Lerato Programs

### 1. Hello World

```lerato
bontsha("Dumela Lefase")
```

### 2. Variables

```lerato
leina = "Lerato"
palo = 10

bontsha(leina)
bontsha(palo)
```

### 3. Arithmetic

```lerato
a = 8
b = 4
sephetho = a * b + 2

bontsha(sephetho)
```

### 4. If Block

```lerato
palo = 7

ge palo > 5 gona
    bontsha("Palo e feta 5")
feleletsa
```

### 5. Function and Return

```lerato
tiro kopanya(a, b) gona
    busa a + b
feleletsa

karabo = kopanya(2, 3)
bontsha(karabo)
```

## 9. 2-Week Implementation Sequence

### Week 1

#### Day 1

- fill in `pyproject.toml`
- create CLI entry point
- add `ast_nodes.py` and `errors.py`
- set up `pytest`

#### Day 2

- define token types
- implement identifier, keyword, number, and string lexing
- add token position tracking

#### Day 3

- finish lexer operators and punctuation
- add lexer tests for keywords and literals
- verify tokenization of `examples/hello.ler`

#### Day 4

- implement expression parsing with precedence
- support literals, identifiers, grouping, and calls

#### Day 5

- implement statement parsing for print and assignment
- add parser tests for valid basic programs

#### Day 6

- implement `if` block parsing with `ge`, `gona`, `feleletsa`
- add parser tests for nested statements

#### Day 7

- implement function definitions and `busa`
- add parser tests for function bodies and parameters

### Week 2

#### Day 8

- implement Python code generation for literals, expressions, and print
- add transpiler string-output tests

#### Day 9

- implement transpilation for assignments and comparisons
- verify generated Python executes correctly

#### Day 10

- implement transpilation for `if` blocks
- add end-to-end test for conditional execution

#### Day 11

- implement transpilation for functions and returns
- add end-to-end function tests

#### Day 12

- implement runtime execution wrapper
- surface syntax and runtime failures with line information

#### Day 13

- wire full CLI path: file -> lexer -> parser -> transpiler -> exec
- run all example `.ler` files through the CLI

#### Day 14

- tighten tests
- fix error messages
- update `README.md` with usage and supported syntax
- declare version 0 prototype complete if all five example programs run

## 10. Immediate First Tasks

1. Create `src/lerato/ast_nodes.py` with dataclasses for statements and expressions.
2. Create `src/lerato/errors.py` with syntax and runtime error classes.
3. Fill in `pyproject.toml` with package metadata and a CLI entry point.
4. Implement the token enum and `Token` dataclass in `lexer.py`.
5. Add lexer support for `bontsha`, `tiro`, `busa`, `ge`, `gona`, `feleletsa`, `nnete`, and `maaka`.
6. Implement lexer tests before writing the parser.
7. Implement expression parsing with precedence in `parser.py`.
8. Implement parsing for assignment, print, `if`, function, and return statements.
9. Implement the first transpiler pass for hello world and assignments.
10. Add an end-to-end test that executes `examples/hello.ler`.

## 11. Testing Strategy

### Priority Order

1. lexer correctness
2. parser correctness
3. transpiler output correctness
4. end-to-end execution

### Required Early Tests

- keywords are recognized correctly
- identifiers are not misclassified as keywords
- numbers and strings tokenize correctly
- `1 + 2 * 3` parses with correct precedence
- `ge ... gona ... feleletsa` parses into one block
- `tiro ... busa ... feleletsa` transpiles to valid Python
- `nnete` and `maaka` map to `True` and `False`
- `examples/hello.ler` executes successfully

### Recommendation

Do exact-string assertions for small transpiler outputs. For version 0, this is simpler and more useful than abstract golden-file infrastructure.

## 12. Risks and Pitfalls

### Ambiguous Grammar

If statement boundaries are too loose, the parser will become fragile. Keep each statement form strict.

### Too Much Natural Language

Do not try to make Lerato parse free-form Sepedi phrases. Use Sepedi-inspired keywords with conventional programming structure.

### Scope Creep

Loops, imports, collections, and better tooling should wait until the five example programs run end to end.

### Keyboard Issues

Do not introduce accented or special characters into keywords. Keep the language ASCII-only until tooling is stable.

## 13. Recommended Decisions

To move fastest, the project should commit to these decisions now:

- Python implementation
- handwritten lexer
- handwritten recursive-descent parser
- transpile to Python, then execute
- explicit block delimiters with `gona` and `feleletsa`
- no indentation-sensitive parsing
- no loops or modules in version 0

If a proposed change does not help deliver the 2-week sequence above, it should be deferred.
