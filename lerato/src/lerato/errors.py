"""Shared error types for the Lerato prototype."""

from __future__ import annotations


class LeratoError(Exception):
    """Base class for all Lerato-specific exceptions."""


class LeratoSyntaxError(LeratoError):
    """Raised when source code is not valid Lerato syntax."""

    def __init__(
        self,
        message: str,
        *,
        line: int | None = None,
        column: int | None = None,
    ) -> None:
        self.line = line
        self.column = column
        super().__init__(self._format_message(message))

    def _format_message(self, message: str) -> str:
        if self.line is None:
            return message
        if self.column is None:
            return f"line {self.line}: {message}"
        return f"line {self.line}, column {self.column}: {message}"


class LeratoRuntimeError(LeratoError):
    """Raised when a Lerato program fails during execution."""
