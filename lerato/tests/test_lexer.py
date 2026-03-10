from lerato.errors import LeratoSyntaxError
from lerato.lexer import TokenType, tokenize


def token_types(source: str) -> list[TokenType]:
    return [token.token_type for token in tokenize(source)]


def test_lexes_keywords_and_eof() -> None:
    tokens = tokenize("bontsha tiro busa ge goba gefela gona feleletsa nnete maaka")

    assert [token.token_type for token in tokens] == [
        TokenType.BONTSHA,
        TokenType.TIRO,
        TokenType.BUSA,
        TokenType.GE,
        TokenType.GOBA,
        TokenType.GEFELA,
        TokenType.GONA,
        TokenType.FELELETSA,
        TokenType.NNETE,
        TokenType.MAAKA,
        TokenType.EOF,
    ]


def test_identifiers_do_not_collide_with_keywords() -> None:
    tokens = tokenize("bontshana geza tiro_1")

    assert [token.token_type for token in tokens] == [
        TokenType.IDENTIFIER,
        TokenType.IDENTIFIER,
        TokenType.IDENTIFIER,
        TokenType.EOF,
    ]


def test_lexes_strings_numbers_and_operators() -> None:
    tokens = tokenize('x = 12 + 3.5\nbontsha("Dumela")\nge x >= 3 gona')

    assert [token.token_type for token in tokens] == [
        TokenType.IDENTIFIER,
        TokenType.EQUAL,
        TokenType.NUMBER,
        TokenType.PLUS,
        TokenType.NUMBER,
        TokenType.NEWLINE,
        TokenType.BONTSHA,
        TokenType.LEFT_PAREN,
        TokenType.STRING,
        TokenType.RIGHT_PAREN,
        TokenType.NEWLINE,
        TokenType.GE,
        TokenType.IDENTIFIER,
        TokenType.GREATER_EQUAL,
        TokenType.NUMBER,
        TokenType.GONA,
        TokenType.EOF,
    ]
    assert tokens[2].literal == 12
    assert tokens[4].literal == 3.5
    assert tokens[8].literal == "Dumela"


def test_tracks_line_and_column_positions() -> None:
    tokens = tokenize("x = 1\nbontsha(x)\n")

    assert tokens[0].line == 1
    assert tokens[0].column == 1
    assert tokens[4].token_type == TokenType.BONTSHA
    assert tokens[4].line == 2
    assert tokens[4].column == 1


def test_raises_for_unterminated_string() -> None:
    try:
        tokenize('bontsha("Dumela)')
    except LeratoSyntaxError as exc:
        assert "unterminated string" in str(exc)
        assert exc.line == 1
        assert exc.column == 9
    else:
        raise AssertionError("expected LeratoSyntaxError")


def test_raises_for_invalid_character() -> None:
    try:
        tokenize("@")
    except LeratoSyntaxError as exc:
        assert "unexpected character" in str(exc)
        assert exc.line == 1
        assert exc.column == 1
    else:
        raise AssertionError("expected LeratoSyntaxError")
