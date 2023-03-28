from dataclasses import dataclass


@dataclass
class StringToken:
    VARIABLE = 0
    LEFT_BRACKET = 1
    RIGHT_BRACKET = 2
    INVERSION = 3
    CONJUNCTION = 4
    DISJUNCTION = 5
    IMPLICATION = 6
    EQUIVALENCE = 7
