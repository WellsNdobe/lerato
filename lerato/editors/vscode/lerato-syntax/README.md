# Lerato Syntax for VS Code

This extension adds syntax highlighting for `.ler` files.

## Included

- Lerato keywords such as `ge`, `goba`, `gefela`, `tiro`, `busa`, and `tsenya`
- built-in functions such as `bontsha(...)` and `amogela(...)`
- strings, numbers, booleans, operators, and function names

## Run With F5

If you opened the repository root in VS Code, use the `Run Lerato Syntax Extension`
launch configuration and press `F5`. That starts an Extension Development Host for
the nested extension in `editors/vscode/lerato-syntax`.

If you opened only the extension folder itself in VS Code, pressing `F5` should
also work directly.

## Install Locally

1. Open this folder in VS Code:
   `editors/vscode/lerato-syntax`
2. Run `powershell -ExecutionPolicy Bypass -File .\package-extension.ps1`.
3. In VS Code, install the generated `.vsix` file with:
   `Extensions: Install from VSIX...`

If you already use `vsce`, `vsce package` should also work.

For quick local development, you can also open the extension folder in VS Code and run the extension in an Extension Development Host with `F5`.
