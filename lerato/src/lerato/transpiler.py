"""Transpile Lerato ASTs into Python source."""

from __future__ import annotations

from lerato.ast_nodes import (
    AssignStmt,
    BinaryExpr,
    BooleanLiteral,
    CallExpr,
    ExprStmt,
    Expression,
    FunctionDefStmt,
    Identifier,
    ImportStmt,
    IfStmt,
    NumberLiteral,
    PrintStmt,
    Program,
    ReturnStmt,
    Statement,
    StringLiteral,
    UnaryExpr,
    WhileStmt,
)
from lerato.parser import parse_program


class Transpiler:
    def transpile_program(self, program: Program) -> str:
        lines: list[str] = []
        for statement in program.statements:
            lines.extend(self._statement(statement, 0))
        return "\n".join(lines) + ("\n" if lines else "")

    def _statement(self, statement: Statement, indent_level: int) -> list[str]:
        indent = "    " * indent_level

        if isinstance(statement, PrintStmt):
            return [f"{indent}print({self._expression(statement.expression)})"]
        if isinstance(statement, ImportStmt):
            return [f"{indent}__lerato_import__({statement.path!r})"]
        if isinstance(statement, AssignStmt):
            return [f"{indent}{statement.name} = {self._expression(statement.expression)}"]
        if isinstance(statement, ReturnStmt):
            return [f"{indent}return {self._expression(statement.expression)}"]
        if isinstance(statement, ExprStmt):
            return [f"{indent}{self._expression(statement.expression)}"]
        if isinstance(statement, IfStmt):
            lines = [f"{indent}if {self._expression(statement.condition)}:"]
            lines.extend(self._block(statement.body, indent_level + 1))
            if statement.else_body:
                lines.append(f"{indent}else:")
                lines.extend(self._block(statement.else_body, indent_level + 1))
            return lines
        if isinstance(statement, WhileStmt):
            lines = [f"{indent}while {self._expression(statement.condition)}:"]
            lines.extend(self._block(statement.body, indent_level + 1))
            return lines
        if isinstance(statement, FunctionDefStmt):
            params = ", ".join(statement.params)
            lines = [f"{indent}def {statement.name}({params}):"]
            lines.extend(self._block(statement.body, indent_level + 1))
            return lines

        raise TypeError(f"unsupported statement node: {type(statement).__name__}")

    def _block(self, statements: list[Statement], indent_level: int) -> list[str]:
        if not statements:
            return [f'{"    " * indent_level}pass']

        lines: list[str] = []
        for statement in statements:
            lines.extend(self._statement(statement, indent_level))
        return lines

    def _expression(self, expression: Expression) -> str:
        if isinstance(expression, Identifier):
            return expression.name
        if isinstance(expression, NumberLiteral):
            return str(expression.value)
        if isinstance(expression, StringLiteral):
            return repr(expression.value)
        if isinstance(expression, BooleanLiteral):
            return "True" if expression.value else "False"
        if isinstance(expression, UnaryExpr):
            return f"{expression.operator}{self._parenthesize_if_needed(expression.operand)}"
        if isinstance(expression, BinaryExpr):
            left = self._parenthesize_if_binary(expression.left)
            right = self._parenthesize_if_binary(expression.right)
            return f"{left} {expression.operator} {right}"
        if isinstance(expression, CallExpr):
            args = ", ".join(self._expression(arg) for arg in expression.args)
            return f"{expression.callee}({args})"

        raise TypeError(f"unsupported expression node: {type(expression).__name__}")

    def _parenthesize_if_binary(self, expression: Expression) -> str:
        rendered = self._expression(expression)
        if isinstance(expression, BinaryExpr):
            return f"({rendered})"
        return rendered

    def _parenthesize_if_needed(self, expression: Expression) -> str:
        rendered = self._expression(expression)
        if isinstance(expression, BinaryExpr):
            return f"({rendered})"
        return rendered


def transpile(program: Program) -> str:
    return Transpiler().transpile_program(program)


def transpile_source(source: str) -> str:
    return transpile(parse_program(source))
