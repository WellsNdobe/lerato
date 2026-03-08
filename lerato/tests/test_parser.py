from lerato.ast_nodes import (
    BinaryExpr,
    BooleanLiteral,
    CallExpr,
    Identifier,
    NumberLiteral,
    StringLiteral,
    UnaryExpr,
)
from lerato.errors import LeratoSyntaxError
from lerato.parser import parse_expression


def test_parses_arithmetic_precedence() -> None:
    expression = parse_expression("1 + 2 * 3")

    assert isinstance(expression, BinaryExpr)
    assert expression.operator == "+"
    assert isinstance(expression.left, NumberLiteral)
    assert expression.left.value == 1
    assert isinstance(expression.right, BinaryExpr)
    assert expression.right.operator == "*"


def test_grouping_changes_precedence() -> None:
    expression = parse_expression("(1 + 2) * 3")

    assert isinstance(expression, BinaryExpr)
    assert expression.operator == "*"
    assert isinstance(expression.left, BinaryExpr)
    assert expression.left.operator == "+"


def test_parses_boolean_literals() -> None:
    true_expr = parse_expression("nnete")
    false_expr = parse_expression("maaka")

    assert isinstance(true_expr, BooleanLiteral)
    assert true_expr.value is True
    assert isinstance(false_expr, BooleanLiteral)
    assert false_expr.value is False


def test_parses_unary_minus() -> None:
    expression = parse_expression("-12")

    assert isinstance(expression, UnaryExpr)
    assert expression.operator == "-"
    assert isinstance(expression.operand, NumberLiteral)
    assert expression.operand.value == 12


def test_parses_identifier_and_call_expression() -> None:
    identifier = parse_expression("karabo")
    call = parse_expression('kopanya(1, "pedi", nnete)')

    assert isinstance(identifier, Identifier)
    assert identifier.name == "karabo"
    assert isinstance(call, CallExpr)
    assert call.callee == "kopanya"
    assert len(call.args) == 3
    assert isinstance(call.args[0], NumberLiteral)
    assert isinstance(call.args[1], StringLiteral)
    assert isinstance(call.args[2], BooleanLiteral)


def test_parses_comparison_and_equality() -> None:
    expression = parse_expression("x + 1 >= y == nnete")

    assert isinstance(expression, BinaryExpr)
    assert expression.operator == "=="
    assert isinstance(expression.left, BinaryExpr)
    assert expression.left.operator == ">="
    assert isinstance(expression.right, BooleanLiteral)


def test_raises_on_missing_closing_paren() -> None:
    try:
        parse_expression("(1 + 2")
    except LeratoSyntaxError as exc:
        assert "expected ')'" in str(exc)
    else:
        raise AssertionError("expected LeratoSyntaxError")


def test_raises_on_trailing_tokens() -> None:
    try:
        parse_expression("1 2")
    except LeratoSyntaxError as exc:
        assert "unexpected token" in str(exc)
    else:
        raise AssertionError("expected LeratoSyntaxError")
