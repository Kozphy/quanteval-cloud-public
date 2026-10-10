class QuantEvalError(Exception):
    """Base error."""


class DataValidationError(QuantEvalError):
    """Input data failed hard validation checks."""

    def __init__(self, errors: list[str]):
        self.errors = list(errors)
        super().__init__("Input data failed validation:\n  - " + "\n  - ".join(self.errors))


class QuotaError(QuantEvalError):
    """A configured limit (rows, size, lookback, horizon, origins, timeout) was exceeded."""


class LeakageError(QuantEvalError):
    """A look-ahead / train-test separation violation was detected."""


class ComplianceError(QuantEvalError):
    """Rendered report contains language that is not allowed (e.g. trade instructions)."""
