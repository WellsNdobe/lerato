"""Shared error types for the Lerato prototype."""

from __future__ import annotations


class LeratoError(Exception):
    """Base class for all Lerato-specific exceptions."""


def format_bilingual_message(
    english_message: str,
    *,
    sepedi_message: str | None = None,
    line: int | None = None,
    column: int | None = None,
) -> str:
    location = ""
    if line is not None and column is not None:
        location = f"line {line}, column {column}: "
    elif line is not None:
        location = f"line {line}: "

    sepedi = sepedi_message or english_message
    return (
        f"{location}Sepedi: {sepedi}\n"
        f"{location}English: {english_message}"
    )


class LeratoSyntaxError(LeratoError):
    """Raised when source code is not valid Lerato syntax."""

    def __init__(
        self,
        message: str,
        *,
        sepedi_message: str | None = None,
        line: int | None = None,
        column: int | None = None,
    ) -> None:
        self.line = line
        self.column = column
        super().__init__(
            format_bilingual_message(
                message,
                sepedi_message=sepedi_message,
                line=line,
                column=column,
            )
        )


class LeratoRuntimeError(LeratoError):
    """Raised when a Lerato program fails during execution."""

    def __init__(
        self,
        message: str,
        *,
        sepedi_message: str | None = None,
        line: int | None = None,
        column: int | None = None,
    ) -> None:
        self.line = line
        self.column = column
        super().__init__(
            format_bilingual_message(
                message,
                sepedi_message=sepedi_message,
                line=line,
                column=column,
            )
        )
