from lerato.errors import LeratoRuntimeError
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


def test_runtime_reports_bilingual_keyword_typo_hint() -> None:
    try:
        execute_source('bontsh("Dumela")\n')
    except LeratoRuntimeError as exc:
        message = str(exc)
        assert "Sepedi:" in message
        assert "English:" in message
        assert "bontsh" in message
        assert "bontsha" in message
    else:
        raise AssertionError("expected LeratoRuntimeError")
