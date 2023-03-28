from dataclasses import dataclass
from logic_formula_scripts.string_token import StringToken


@dataclass
class Token:
    token_type: StringToken
    value: str
    order: int
