from dataclasses import dataclass


@dataclass
class FullLogicalResult:
    logical_interpretation: dict
    formula_value: int
