from lerato.ast_nodes import (
    AssignStmt,
    BinaryExpr,
    BooleanLiteral,
    CallExpr,
    Identifier,
    IfStmt,
    NumberLiteral,
    PrintStmt,
    Program,
    ReturnStmt,
    StringLiteral,
    FunctionDefStmt,
    UnaryExpr,
)
from lerato.errors import LeratoSyntaxError
from lerato.parser import parse_expression, parse_program


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


def test_parses_program_with_print_and_assignment() -> None:
    program = parse_program('x = 3\nbontsha(x)\n')

    assert isinstance(program, Program)
    assert len(program.statements) == 2
    assert isinstance(program.statements[0], AssignStmt)
    assert program.statements[0].name == "x"
    assert isinstance(program.statements[1], PrintStmt)


def test_parses_if_block() -> None:
    program = parse_program(
        "ge x > 5 gona\n"
        'bontsha("kgolo")\n'
        "feleletsa\n"
    )

    statement = program.statements[0]
    assert isinstance(statement, IfStmt)
    assert isinstance(statement.condition, BinaryExpr)
    assert len(statement.body) == 1
    assert isinstance(statement.body[0], PrintStmt)


def test_parses_function_definition_and_return() -> None:
    program = parse_program(
        "tiro kopanya(a, b) gona\n"
        "busa a + b\n"
        "feleletsa\n"
    )

    statement = program.statements[0]
    assert isinstance(statement, FunctionDefStmt)
    assert statement.name == "kopanya"
    assert statement.params == ["a", "b"]
    assert len(statement.body) == 1
    assert isinstance(statement.body[0], ReturnStmt)


def test_parses_nested_blocks() -> None:
    program = parse_program(
        "tiro lekola(x) gona\n"
        "ge x >= 1 gona\n"
        "busa nnete\n"
        "feleletsa\n"
        "busa maaka\n"
        "feleletsa\n"
    )

    function = program.statements[0]
    assert isinstance(function, FunctionDefStmt)
    assert len(function.body) == 2
    assert isinstance(function.body[0], IfStmt)
    assert isinstance(function.body[1], ReturnStmt)


def test_raises_on_missing_feleletsa() -> None:
    try:
        parse_program("ge nnete gona\nbontsha(\"ee\")\n")
    except LeratoSyntaxError as exc:
        assert "expected 'feleletsa'" in str(exc)
    else:
        raise AssertionError("expected LeratoSyntaxError")


def test_raises_on_missing_newline_after_gona() -> None:
    try:
        parse_program('ge nnete gona bontsha("ee")\nfeleletsa\n')
    except LeratoSyntaxError as exc:
        assert "expected newline after 'gona'" in str(exc)
    else:
        raise AssertionError("expected LeratoSyntaxError")
