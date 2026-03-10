"""Lexer for the Lerato version 0 prototype."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from lerato.errors import LeratoSyntaxError


class TokenType(Enum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    COMMA = auto()
    NEWLINE = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    BANG_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    BONTSHA = auto()
    TIRO = auto()
    BUSA = auto()
    GE = auto()
    GOBA = auto()
    GEFELA = auto()
    GONA = auto()
    TSENYA = auto()
    FELELETSA = auto()
    NNETE = auto()
    MAAKA = auto()

    EOF = auto()


KEYWORDS = {
    "bontsha": TokenType.BONTSHA,
    "tiro": TokenType.TIRO,
    "busa": TokenType.BUSA,
    "ge": TokenType.GE,
    "goba": TokenType.GOBA,
    "gefela": TokenType.GEFELA,
    "gona": TokenType.GONA,
    "tsenya": TokenType.TSENYA,
    "feleletsa": TokenType.FELELETSA,
    "nnete": TokenType.NNETE,
    "maaka": TokenType.MAAKA,
}


@dataclass(slots=True, frozen=True)
class Token:
    token_type: TokenType
    lexeme: str
    literal: object | None
    line: int
    column: int


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.start_line = 1
        self.start_column = 1

    def tokenize(self) -> list[Token]:
        while not self._is_at_end():
            self.start = self.current
            self.start_line = self.line
            self.start_column = self.column
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.column))
        return self.tokens

    def _scan_token(self) -> None:
        char = self._advance()

        match char:
            case "(":
                self._add_token(TokenType.LEFT_PAREN)
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
            case ",":
                self._add_token(TokenType.COMMA)
            case "\n":
                self._add_token(TokenType.NEWLINE)
            case " " | "\r" | "\t":
                return
            case "+":
                self._add_token(TokenType.PLUS)
            case "-":
                self._add_token(TokenType.MINUS)
            case "*":
                self._add_token(TokenType.STAR)
            case "/":
                self._add_token(TokenType.SLASH)
            case "=":
                token_type = TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
                self._add_token(token_type)
            case "!":
                if self._match("="):
                    self._add_token(TokenType.BANG_EQUAL)
                    return
                self._error("unexpected character '!'")
            case ">":
                token_type = TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
                self._add_token(token_type)
            case "<":
                token_type = TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
                self._add_token(token_type)
            case '"':
                self._string()
            case _:
                if char.isdigit():
                    self._number()
                    return
                if self._is_identifier_start(char):
                    self._identifier()
                    return
                self._error(f"unexpected character {char!r}")

    def _identifier(self) -> None:
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()

        lexeme = self.source[self.start : self.current]
        token_type = KEYWORDS.get(lexeme, TokenType.IDENTIFIER)
        self._add_token(token_type)

    def _number(self) -> None:
        while self._peek().isdigit():
            self._advance()

        literal: int | float
        if self._peek() == "." and self._peek_next().isdigit():
            self._advance()
            while self._peek().isdigit():
                self._advance()
            lexeme = self.source[self.start : self.current]
            literal = float(lexeme)
        else:
            lexeme = self.source[self.start : self.current]
            literal = int(lexeme)

        self._add_token(TokenType.NUMBER, literal)

    def _string(self) -> None:
        while self._peek() != '"' and not self._is_at_end():
            self._advance()

        if self._is_at_end():
            self._error("unterminated string")

        self._advance()
        lexeme = self.source[self.start : self.current]
        literal = lexeme[1:-1]
        self._add_token(TokenType.STRING, literal)

    def _add_token(self, token_type: TokenType, literal: object | None = None) -> None:
        lexeme = self.source[self.start : self.current]
        self.tokens.append(
            Token(
                token_type=token_type,
                lexeme=lexeme,
                literal=literal,
                line=self.start_line,
                column=self.start_column,
            )
        )

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        self.column += 1
        return True

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _is_identifier_start(self, char: str) -> bool:
        return char.isalpha() or char == "_"

    def _error(self, message: str) -> None:
        sepedi_message = {
            "unterminated string": "Mothalo wa sengwalwa ga se wa tswalelwa.",
        }.get(message, f"Go na le seka seo se sa amogelwego: {message}")
        raise LeratoSyntaxError(
            message,
            sepedi_message=sepedi_message,
            line=self.start_line,
            column=self.start_column,
        )


def tokenize(source: str) -> list[Token]:
    return Lexer(source).tokenize()
