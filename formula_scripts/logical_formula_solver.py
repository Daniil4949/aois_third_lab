from itertools import product
from logic_formula_scripts.string_token import StringToken
from logic_formula_scripts.token import Token
from logic_formula_scripts.logic_values import ORDER, SYMBOLS
from logic_formula_scripts.interpretation import FullLogicalResult


class TruthTableSolver:

    def __init__(self, raw_formula: str):
        self.token_list: list[Token] = []
        self.initial_formula: str = raw_formula
        self.logic_values: set[str] = set()
        self.operation_stack: (list[Token], None) = []
        self.value_stack: (list[int], None) = []

    def __specify_token(self, raw_token, symbol):
        if not raw_token == '':
            self.token_list.append(Token(StringToken.VARIABLE, raw_token, ORDER[StringToken.VARIABLE]))
            self.logic_values.add(raw_token)
        raw_token = ''
        new_token_type = SYMBOLS[symbol]
        self.token_list.append(Token(new_token_type, symbol, ORDER[new_token_type]))
        return raw_token

    @staticmethod
    def format_formula(formula) -> str:
        formula = formula.replace('^', '∧')
        formula = formula.replace('&', '∧')
        formula = formula.replace('*', '∧')
        formula = formula.replace('+', '∨')
        formula = formula.replace('|', '∨')
        return formula

    def __check_symbol(self, symbol, raw_token):
        if symbol.isdigit() and len(raw_token) == 0:
            print('Numbers can go only after letters')
        elif symbol.isalpha() or symbol.isdigit():
            raw_token += symbol
        elif SYMBOLS.get(symbol, None):
            raw_token = self.__specify_token(raw_token, symbol)
        return raw_token

    def __divide_into_tokens(self):
        self.initial_formula = self.format_formula(self.initial_formula)
        raw_token: str = ''
        for symbol in self.initial_formula:
            raw_token = self.__check_symbol(symbol, raw_token)
            if symbol.isspace():
                continue
        if not raw_token == '':
            self.token_list.append(Token(StringToken.VARIABLE, raw_token, ORDER[StringToken.VARIABLE]))
            self.logic_values.add(raw_token)
        self.logic_values = sorted(self.logic_values)

    def __check_inversion(self):
        if self.operation_stack[len(self.operation_stack) - 1].token_type == StringToken.INVERSION:
            self.value_stack.append(int(not self.value_stack.pop()))
            self.operation_stack.pop()
            return False
        else:
            return True

    def __solve_operation(self):
        if self.__check_inversion():
            first_value: int = self.value_stack.pop()
            second_value: int = self.value_stack.pop()
            if self.operation_stack[len(self.operation_stack) - 1].token_type == StringToken.CONJUNCTION:
                self.value_stack.append(first_value & second_value)
            elif self.operation_stack[len(self.operation_stack) - 1].token_type == StringToken.DISJUNCTION:
                self.value_stack.append(first_value | second_value)
            elif self.operation_stack[len(self.operation_stack) - 1].token_type == StringToken.IMPLICATION:
                self.value_stack.append(int(not second_value) | first_value)
            elif self.operation_stack[len(self.operation_stack) - 1].token_type == StringToken.EQUIVALENCE:
                self.value_stack.append((int(not second_value) & int(not first_value)) | (second_value & first_value))
            self.operation_stack.pop()
        else:
            return

    def __iterate_logic_formula(self, token):
        while (not token.order < self.operation_stack[len(self.operation_stack) - 1].order) and \
                (self.operation_stack[
                     len(self.operation_stack) - 1].token_type != StringToken.LEFT_BRACKET):
            self.__solve_operation()
        self.operation_stack.append(token)

    def __check_end_of_logic_formula(self):
        while not self.operation_stack[len(self.operation_stack) - 1].token_type == StringToken.LEFT_BRACKET:
            self.__solve_operation()
        self.operation_stack.pop()

    def __iterate_sub_formula(self, token):
        if len(self.operation_stack) == 0 or self.operation_stack[len(self.operation_stack) - 1].token_type == \
                StringToken.LEFT_BRACKET:
            self.operation_stack.append(token)
        else:
            self.__iterate_logic_formula(token)

    def __solve_for_interpretation(self, logical_interpretation: dict):
        for token in self.token_list:
            if token.token_type == StringToken.VARIABLE:
                self.value_stack.append(logical_interpretation[token.value])
            elif token.token_type == StringToken.LEFT_BRACKET:
                self.operation_stack.append(token)
            elif token.token_type in (StringToken.INVERSION, StringToken.CONJUNCTION, StringToken.DISJUNCTION,
                                      StringToken.IMPLICATION, StringToken.EQUIVALENCE):
                self.__iterate_sub_formula(token)
            elif token.token_type == StringToken.RIGHT_BRACKET:
                self.__check_end_of_logic_formula()
        while len(self.operation_stack) != 0:
            self.__solve_operation()
        return FullLogicalResult(logical_interpretation, self.value_stack.pop())

    def __extend_logic_table(self, item, raw_truth_table):
        logical_interpretation = dict(zip(self.logic_values, item))
        raw_truth_table.append(self.__solve_for_interpretation(logical_interpretation))

    def solve_formula(self):
        self.__divide_into_tokens()
        possible_var_combs = sorted(list(product([0, 1], repeat=len(self.logic_values))))
        raw_truth_table: list[FullLogicalResult] = list()
        for item in possible_var_combs:
            self.__extend_logic_table(item, raw_truth_table)
        return raw_truth_table

    def present_result_table(self):
        raw_truth_table = self.solve_formula()
        for var in self.logic_values:
            print(var.center(len(var) + 2, ' '), end="")
        print(self.initial_formula.center(len(self.initial_formula) + 2, ' '))
        for interpretation in raw_truth_table:
            for var, value in interpretation.logical_interpretation.items():
                print(str(value).center(len(var) + 2, ' '), end='')
            print(str(interpretation.formula_value).center(len(self.initial_formula) + 2, ' '))
