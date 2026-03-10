from lerato.errors import LeratoRuntimeError
from lerato.runtime import execute_file, execute_source, transpile_for_execution


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


def test_runtime_supports_input_builtin(monkeypatch, capsys) -> None:
    monkeypatch.setattr("builtins.input", lambda prompt="": "Lerato")

    execute_source('leina = amogela("Leina: ")\nbontsha(leina)\n')

    captured = capsys.readouterr()
    assert captured.out.strip() == "Lerato"


def test_runtime_imports_other_lerato_files(capsys) -> None:
    execute_file("examples/import_demo.ler")

    captured = capsys.readouterr()
    assert captured.out.strip() == "5"


def test_runtime_reports_missing_import_file() -> None:
    try:
        execute_source('tsenya "missing.ler"\n')
    except LeratoRuntimeError as exc:
        assert "imported file not found" in str(exc)
    else:
        raise AssertionError("expected LeratoRuntimeError")


def test_runtime_executes_if_else_and_while(capsys) -> None:
    execute_source(
        "x = 0\n"
        "gefela x < 3 gona\n"
        "ge x == 1 gona\n"
        'bontsha("magareng")\n'
        "goba\n"
        "bontsha(x)\n"
        "feleletsa\n"
        "x = x + 1\n"
        "feleletsa\n"
    )

    captured = capsys.readouterr()
    assert captured.out.strip().splitlines() == ["0", "magareng", "2"]


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
