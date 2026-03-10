
"""AST nodes for the Lerato version 0 prototype."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Node:
    """Base type for all AST nodes."""


@dataclass(slots=True)
class Statement(Node):
    """Base type for AST statements."""


@dataclass(slots=True)
class Expression(Node):
    """Base type for AST expressions."""


@dataclass(slots=True)
class Program(Node):
    statements: list[Statement] = field(default_factory=list)


@dataclass(slots=True)
class PrintStmt(Statement):
    expression: Expression


@dataclass(slots=True)
class AssignStmt(Statement):
    name: str
    expression: Expression


@dataclass(slots=True)
class IfStmt(Statement):
    condition: Expression
    body: list[Statement] = field(default_factory=list)
    else_body: list[Statement] = field(default_factory=list)


@dataclass(slots=True)
class WhileStmt(Statement):
    condition: Expression
    body: list[Statement] = field(default_factory=list)


@dataclass(slots=True)
class FunctionDefStmt(Statement):
    name: str
    params: list[str] = field(default_factory=list)
    body: list[Statement] = field(default_factory=list)


@dataclass(slots=True)
class ReturnStmt(Statement):
    expression: Expression


@dataclass(slots=True)
class ExprStmt(Statement):
    expression: Expression


@dataclass(slots=True)
class BinaryExpr(Expression):
    left: Expression
    operator: str
    right: Expression


@dataclass(slots=True)
class UnaryExpr(Expression):
    operator: str
    operand: Expression


@dataclass(slots=True)
class CallExpr(Expression):
    callee: str
    args: list[Expression] = field(default_factory=list)


@dataclass(slots=True)
class Identifier(Expression):
    name: str


@dataclass(slots=True)
class NumberLiteral(Expression):
    value: int | float


@dataclass(slots=True)
class StringLiteral(Expression):
    value: str


@dataclass(slots=True)
class BooleanLiteral(Expression):
    value: bool
