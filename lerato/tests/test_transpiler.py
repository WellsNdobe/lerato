from lerato.transpiler import transpile_source


def test_transpiles_hello_world() -> None:
    python_source = transpile_source('bontsha("Dumela Lefase")\n')

    assert python_source == "print('Dumela Lefase')\n"


def test_transpiles_assignment_and_arithmetic() -> None:
    python_source = transpile_source("x = 1 + 2 * 3\n")

    assert python_source == "x = 1 + (2 * 3)\n"


def test_transpiles_if_block() -> None:
    python_source = transpile_source(
        "ge nnete gona\n"
        'bontsha("ee")\n'
        "feleletsa\n"
    )

    assert python_source == "if True:\n    print('ee')\n"


def test_transpiles_if_else_block() -> None:
    python_source = transpile_source(
        "ge nnete gona\n"
        'bontsha("ee")\n'
        "goba\n"
        'bontsha("aowa")\n'
        "feleletsa\n"
    )

    assert python_source == "if True:\n    print('ee')\nelse:\n    print('aowa')\n"


def test_transpiles_while_block() -> None:
    python_source = transpile_source(
        "gefela x < 3 gona\n"
        "x = x + 1\n"
        "feleletsa\n"
    )

    assert python_source == "while x < 3:\n    x = x + 1\n"


def test_transpiles_function_definition_and_return() -> None:
    python_source = transpile_source(
        "tiro kopanya(a, b) gona\n"
        "busa a + b\n"
        "feleletsa\n"
    )

    assert python_source == "def kopanya(a, b):\n    return a + b\n"


def test_transpiles_call_expression_statement() -> None:
    python_source = transpile_source("kopanya(2, 3)\n")

    assert python_source == "kopanya(2, 3)\n"


def test_transpiles_nested_block_structure() -> None:
    python_source = transpile_source(
        "tiro lekola(x) gona\n"
        "ge x >= 1 gona\n"
        "busa nnete\n"
        "feleletsa\n"
        "busa maaka\n"
        "feleletsa\n"
    )

    assert python_source == (
        "def lekola(x):\n"
        "    if x >= 1:\n"
        "        return True\n"
        "    return False\n"
    )
