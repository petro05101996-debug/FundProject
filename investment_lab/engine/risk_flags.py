"""Structured risk-flag model and constructors."""
from __future__ import annotations

from dataclasses import asdict, dataclass

from investment_lab.domain.enums import RiskFlagCode, Severity


@dataclass(frozen=True)
class RiskFlag:
    scenario: str
    severity: str
    code: str
    title: str
    description: str
    metric: str = "—"
    limit: str = "—"

    def as_dict(self) -> dict[str, str]:
        data = asdict(self)
        data["flag"] = self.description
        return data


def make_flag(scenario: str, code: RiskFlagCode | str, severity: Severity | str, title: str, description: str, metric: str = "—", limit: str = "—") -> dict[str, str]:
    code_value = code.value if isinstance(code, RiskFlagCode) else str(code)
    severity_value = severity.value if isinstance(severity, Severity) else str(severity)
    return RiskFlag(scenario, severity_value, code_value, title, description, metric, limit).as_dict()
