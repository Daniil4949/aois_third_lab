from logic_formula_scripts.string_token import StringToken

SYMBOLS: dict = {'(': StringToken.LEFT_BRACKET, ')': StringToken.RIGHT_BRACKET, '!': StringToken.INVERSION,
                 '&': StringToken.CONJUNCTION, '∧': StringToken.CONJUNCTION,
                 '∨': StringToken.DISJUNCTION, '->': StringToken.IMPLICATION,
                 '<->': StringToken.EQUIVALENCE}

ORDER: dict = {StringToken.VARIABLE: -1, StringToken.LEFT_BRACKET: -1, StringToken.RIGHT_BRACKET: -1,
               StringToken.INVERSION: 0, StringToken.CONJUNCTION: 1, StringToken.DISJUNCTION: 1,
               StringToken.IMPLICATION: 3, StringToken.EQUIVALENCE: 4}
