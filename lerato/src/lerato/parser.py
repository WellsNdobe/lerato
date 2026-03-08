"""Parser for Lerato expressions."""

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
    IfStmt,
    NumberLiteral,
    PrintStmt,
    Program,
    ReturnStmt,
    Statement,
    StringLiteral,
    UnaryExpr,
)
from lerato.errors import LeratoSyntaxError
from lerato.lexer import Token, TokenType, tokenize


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def parse_program(self) -> Program:
        statements: list[Statement] = []
        self._skip_newlines()

        while not self._is_at_end():
            statements.append(self._statement())
            self._skip_newlines()

        return Program(statements)

    def parse_expression(self) -> Expression:
        expression = self._equality()
        self._consume_trailing_newlines()
        if not self._is_at_end():
            token = self._peek()
            raise LeratoSyntaxError(
                f"unexpected token {token.lexeme!r}",
                line=token.line,
                column=token.column,
            )
        return expression

    def _statement(self) -> Statement:
        if self._match(TokenType.BONTSHA):
            return self._print_statement()
        if self._match(TokenType.GE):
            return self._if_statement()
        if self._match(TokenType.TIRO):
            return self._function_statement()
        if self._match(TokenType.BUSA):
            return self._return_statement()
        if self._check(TokenType.IDENTIFIER) and self._check_next(TokenType.EQUAL):
            return self._assignment_statement()
        return self._expression_statement()

    def _print_statement(self) -> PrintStmt:
        self._consume(TokenType.LEFT_PAREN, "expected '(' after 'bontsha'")
        expression = self._equality()
        self._consume(TokenType.RIGHT_PAREN, "expected ')' after print expression")
        self._consume_statement_terminator("expected newline after print statement")
        return PrintStmt(expression)

    def _assignment_statement(self) -> AssignStmt:
        name = self._consume(TokenType.IDENTIFIER, "expected variable name")
        self._consume(TokenType.EQUAL, "expected '=' in assignment")
        expression = self._equality()
        self._consume_statement_terminator("expected newline after assignment")
        return AssignStmt(name.lexeme, expression)

    def _if_statement(self) -> IfStmt:
        condition = self._equality()
        self._consume(TokenType.GONA, "expected 'gona' after if condition")
        self._require_block_start("expected newline after 'gona'")
        body = self._block()
        return IfStmt(condition, body)

    def _function_statement(self) -> FunctionDefStmt:
        name = self._consume(TokenType.IDENTIFIER, "expected function name")
        self._consume(TokenType.LEFT_PAREN, "expected '(' after function name")

        params: list[str] = []
        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                param = self._consume(TokenType.IDENTIFIER, "expected parameter name")
                params.append(param.lexeme)
                if not self._match(TokenType.COMMA):
                    break

        self._consume(TokenType.RIGHT_PAREN, "expected ')' after parameter list")
        self._consume(TokenType.GONA, "expected 'gona' after function header")
        self._require_block_start("expected newline after 'gona'")
        body = self._block()
        return FunctionDefStmt(name.lexeme, params, body)

    def _return_statement(self) -> ReturnStmt:
        expression = self._equality()
        self._consume_statement_terminator("expected newline after return statement")
        return ReturnStmt(expression)

    def _expression_statement(self) -> ExprStmt:
        expression = self._equality()
        self._consume_statement_terminator("expected newline after expression")
        return ExprStmt(expression)

    def _block(self) -> list[Statement]:
        statements: list[Statement] = []
        self._skip_newlines()

        while not self._check(TokenType.FELELETSA) and not self._is_at_end():
            statements.append(self._statement())
            self._skip_newlines()

        self._consume(TokenType.FELELETSA, "expected 'feleletsa' to end block")
        self._consume_trailing_newlines()
        return statements

    def _equality(self) -> Expression:
        expression = self._comparison()
        while self._match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator = self._previous().lexeme
            right = self._comparison()
            expression = BinaryExpr(expression, operator, right)
        return expression

    def _comparison(self) -> Expression:
        expression = self._term()
        while self._match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self._previous().lexeme
            right = self._term()
            expression = BinaryExpr(expression, operator, right)
        return expression

    def _term(self) -> Expression:
        expression = self._factor()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous().lexeme
            right = self._factor()
            expression = BinaryExpr(expression, operator, right)
        return expression

    def _factor(self) -> Expression:
        expression = self._unary()
        while self._match(TokenType.STAR, TokenType.SLASH):
            operator = self._previous().lexeme
            right = self._unary()
            expression = BinaryExpr(expression, operator, right)
        return expression

    def _unary(self) -> Expression:
        if self._match(TokenType.MINUS):
            return UnaryExpr(self._previous().lexeme, self._unary())
        return self._call()

    def _call(self) -> Expression:
        expression = self._primary()

        while self._match(TokenType.LEFT_PAREN):
            if not isinstance(expression, Identifier):
                token = self._previous()
                raise LeratoSyntaxError(
                    "only identifiers can be called in version 0",
                    line=token.line,
                    column=token.column,
                )
            expression = self._finish_call(expression)

        return expression

    def _finish_call(self, callee: Identifier) -> CallExpr:
        args: list[Expression] = []
        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                args.append(self._equality())
                if not self._match(TokenType.COMMA):
                    break

        self._consume(TokenType.RIGHT_PAREN, "expected ')' after arguments")
        return CallExpr(callee.name, args)

    def _primary(self) -> Expression:
        if self._match(TokenType.NUMBER):
            return NumberLiteral(self._previous().literal)
        if self._match(TokenType.STRING):
            return StringLiteral(self._previous().literal)
        if self._match(TokenType.NNETE):
            return BooleanLiteral(True)
        if self._match(TokenType.MAAKA):
            return BooleanLiteral(False)
        if self._match(TokenType.IDENTIFIER):
            return Identifier(self._previous().lexeme)
        if self._match(TokenType.LEFT_PAREN):
            expression = self._equality()
            self._consume(TokenType.RIGHT_PAREN, "expected ')' after expression")
            return expression

        token = self._peek()
        raise LeratoSyntaxError(
            f"expected expression, got {token.lexeme!r}",
            line=token.line,
            column=token.column,
        )

    def _match(self, *token_types: TokenType) -> bool:
        for token_type in token_types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        token = self._peek()
        raise LeratoSyntaxError(message, line=token.line, column=token.column)

    def _consume_trailing_newlines(self) -> None:
        while self._match(TokenType.NEWLINE):
            pass

    def _consume_statement_terminator(self, message: str) -> None:
        if self._match(TokenType.NEWLINE) or self._check(TokenType.EOF):
            return

        token = self._peek()
        raise LeratoSyntaxError(message, line=token.line, column=token.column)

    def _require_block_start(self, message: str) -> None:
        if self._match(TokenType.NEWLINE):
            return

        token = self._peek()
        raise LeratoSyntaxError(message, line=token.line, column=token.column)

    def _skip_newlines(self) -> None:
        while self._match(TokenType.NEWLINE):
            pass

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return token_type == TokenType.EOF
        return self._peek().token_type == token_type

    def _check_next(self, token_type: TokenType) -> bool:
        if self.current + 1 >= len(self.tokens):
            return False
        return self.tokens[self.current + 1].token_type == token_type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().token_type == TokenType.EOF

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]


def parse_expression(source: str) -> Expression:
    parser = Parser(tokenize(source))
    return parser.parse_expression()


def parse_program(source: str) -> Program:
    parser = Parser(tokenize(source))
    return parser.parse_program()
