from lerato import __version__
from lerato.cli import main


def test_package_version_exposed() -> None:
    assert __version__ == "0.1.0"


def test_cli_version_flag(capsys) -> None:
    exit_code = main(["--version"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "0.1.0"


def test_cli_executes_lerato_file(tmp_path, capsys) -> None:
    source_file = tmp_path / "hello.ler"
    source_file.write_text('bontsha("Dumela Lefase")\n', encoding="utf-8")

    exit_code = main([str(source_file)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "Dumela Lefase"
