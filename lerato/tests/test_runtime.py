from lerato.runtime import execute_source, transpile_for_execution


def test_runtime_executes_hello_world(capsys) -> None:
    execute_source('bontsha("Dumela Lefase")\n')

    captured = capsys.readouterr()
    assert captured.out.strip() == "Dumela Lefase"


def test_runtime_returns_globals_for_assignments() -> None:
    result = execute_source("x = 1 + 2\n")

    assert result["x"] == 3


def test_runtime_transpile_helper_matches_expected_python() -> None:
    python_source = transpile_for_execution("ge nnete gona\nbontsha(\"ee\")\nfeleletsa\n")

    assert python_source == "if True:\n    print('ee')\n"
