# Lerato Project Plan

## 1. Project Overview

Lerato is a beginner-friendly programming language inspired by Sepedi and designed to be easy to type on standard keyboards. Version 0.1 is now a working prototype with a handwritten lexer, parser, transpiler, runtime, and CLI for single-file `.ler` programs.

The next goal is not app building or packaging. The next goal is to make the language itself more usable for real beginner programs.

## 2. Current Implemented Core

Lerato already supports:

- `bontsha(...)` output
- variable assignment
- numbers, strings, and booleans
- arithmetic and comparison expressions
- `ge ... gona ... feleletsa` conditionals
- `tiro ... gona ... busa ... feleletsa` functions
- single-file CLI execution

## 3. Version 0.2 Language Goals

Version 0.2 should add the next missing language fundamentals:

- `else` support for conditionals
- comment syntax
- logical operators
- loops
- list literals
- a small set of built-in functions
- clearer runtime and syntax errors tied to Lerato source

These features should make Lerato usable for small exercises, branching logic, repetition, and simple data handling.

## 4. Design Principles

- Keep Sepedi-inspired ASCII keywords only.
- Prefer one obvious syntax form per feature.
- Keep blocks explicit with `gona` and `feleletsa`.
- Preserve the current handwritten parser and transpile-to-Python pipeline.
- Add features in a way that keeps errors predictable and teachable.
- Do not add classes, modules, static typing, or package management in version 0.2.

## 5. Proposed Version 0.2 Scope

### In Scope

- `else` branch support
- line comments
- logical operators using `and`, `or`, and `not`
- `while` loops
- list literals and indexing
- built-ins like `tsenya(...)`, `bolelele(...)`, and simple type conversion helpers
- improved source-mapped errors

### Out of Scope

- imports and multi-file execution
- classes and objects
- dictionaries or advanced collections
- `for` loops over iterables
- REPL
- optimization work

## 6. Keyword Policy For Version 0.2

For version 0.2, keep logical operators as standard language operators:

- `and`
- `or`
- `not`

Only control-flow keywords that define Lerato syntax should be translated into Sepedi-inspired forms. That keeps expression parsing simpler and avoids keyword ambiguity in the short term.

Version 0.2 keyword decisions:

- `goba` for `else`
- `gefela` for `while`

## 7. Grammar Expansion Targets

Version 0.2 should expand the grammar in this order:

1. `if` with optional `else`
2. logical expressions with clear precedence for `not`, `and`, and `or`
3. comment handling in the lexer
4. `while` statements
5. list literals: `[1, 2, 3]`
6. indexing: `maina[0]`
7. built-in function calls

Important constraints:

- Comments should be ignored by the parser.
- Logical precedence should be stricter than ad hoc parsing.
- List syntax should follow familiar bracket-based forms.
- Error messages should still point to Lerato line and column information.

## 8. Technical Work Areas

### Lexer

- add tokens for brackets
- add tokens or keyword handling for new control-flow syntax
- add logical operator support for `and`, `or`, and `not`
- support comments

### AST

- add `WhileStmt`
- extend `IfStmt` with optional `else_body`
- add `ListLiteral`
- add `IndexExpr`
- add logical expression coverage if separate from binary expressions

### Parser

- parse optional `else`
- add logical-expression precedence levels
- parse `while`
- parse list literals and indexing

### Transpiler

- transpile `else` blocks
- transpile logical operators safely
- transpile `while`
- transpile lists and indexing
- map new built-ins to Python equivalents carefully

### Runtime

- expose a minimal safe builtin environment
- improve error wrapping so Lerato source locations remain understandable

## 9. Two-Week Version 0.2 Sequence

### Week 1

#### Day 1

- update AST for `else`, loops, and lists
- decide final keywords for new syntax
- add failing tests first

#### Day 2

- add lexer support for comments and new keywords
- add bracket tokens for list syntax
- test tokenization thoroughly

#### Day 3

- implement logical expression parsing with precedence
- add parser tests for `and` / `or` / `not`

#### Day 4

- implement `if ... else ...`
- add nested conditional tests

#### Day 5

- implement `while` parsing
- add loop parser tests

#### Day 6

- implement list literals
- add parser tests for list expressions

#### Day 7

- implement indexing expressions
- add parser tests for nested indexing and invalid index syntax

### Week 2

#### Day 8

- transpile logical expressions and `else`
- add output-based transpiler tests

#### Day 9

- transpile `while`
- add end-to-end loop execution tests

#### Day 10

- transpile lists and indexing
- add execution tests covering reads and updates if supported

#### Day 11

- add built-ins such as input, length, and conversions
- test runtime behavior and failure cases

#### Day 12

- improve runtime and syntax error mapping
- make common beginner mistakes easier to diagnose

#### Day 13

- add example programs using loops, lists, and `else`
- run all examples through the CLI

#### Day 14

- tighten tests
- update `README.md` and `DOCUMENTATION.md`
- declare version 0.2 complete if all new examples run

## 10. Immediate First Tasks

1. Extend the AST for `goba` and `gefela`.
2. Add failing tests for comments, logical operators, `else`, loops, and lists.
3. Extend AST nodes before changing the parser.
4. Implement lexer support for the new syntax.
5. Add parser support in small steps, starting with `else` and logical precedence.

## 11. Testing Strategy

Priority order:

1. lexer correctness
2. parser correctness
3. transpiler output correctness
4. end-to-end execution
5. user-facing error quality

Required new tests:

- comments are ignored correctly
- `if ... else ...` parses and executes correctly
- logical operators respect precedence
- `while` loops stop correctly
- list literals transpile to valid Python
- indexing works for valid positions and fails clearly for invalid ones
- built-ins behave consistently

## 12. Risks and Pitfalls

### Keyword Ambiguity

Do not reuse one word for multiple meanings unless the grammar stays unambiguous. Keeping `and`, `or`, and `not` unchanged reduces this risk.

### Scope Creep

Loops and lists are enough for version 0.2. Do not pull in modules, classes, or advanced tooling.

### Error Regressions

Each new syntax feature can make parse errors harder to read. Keep strict tests around line and column reporting.

### Unsafe Runtime Growth

If more built-ins are exposed, keep the execution environment narrow and intentional.

## 13. Recommended Decisions

To keep momentum, the project should commit to these decisions for version 0.2:

- keep Python as the implementation language
- keep the handwritten lexer and parser
- keep transpilation to Python
- keep explicit block delimiters
- add features in the order: `else`, comments, logic, loops, lists, built-ins
- defer imports, classes, and advanced collections
