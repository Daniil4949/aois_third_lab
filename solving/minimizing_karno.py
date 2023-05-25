from typing import List, Dict
from collections import deque
from solving.expression_handler import ExpressionHandler
from solving.truth_table import TruthTableHandler
from solving.logic_calculator import LogicCalculator
from solving.context import TruthTableRow


def logical_expression_result(logic_expression):
    vars_values: Dict[str, bool] = {}
    result_of_expression: List[bool] = []
    signs_of_stack = deque()
    stack_variables = deque()
    tokens: List[str] = []
    all_variables: List[str] = []
    unique_variables: List[str] = []
    ExpressionHandler.counting_variables_of_expression(logic_expression, unique_variables, all_variables)
    ExpressionHandler.dividing_on_tokens(logic_expression, tokens, all_variables)
    number_of_variables: int = len(unique_variables)
    number_of_permutations: int = 2 ** number_of_variables
    truth_table = TruthTableHandler.permutation(number_of_variables)
    if ExpressionHandler.expression_correct(logic_expression, tokens, unique_variables):
        for i in range(number_of_permutations):
            for j in range(number_of_variables):
                vars_values[unique_variables[j]] = truth_table[i][j]
            result_of_expression.append(
                LogicCalculator.calculating(tokens, unique_variables, vars_values, signs_of_stack, stack_variables))
        res: list = []
        for element in range(len(result_of_expression)):
            interpretation = dict()
            for i in range(len(unique_variables)):
                interpretation[unique_variables[i]] = int(truth_table[element][i])
            x = TruthTableRow(value=int(result_of_expression[element]), interpretation=interpretation)
            res.append(x)
        return res


GREI_CODE = {'00': 1, '01': 2, '11': 3, '10': 4}


class Karnough:
    CONJUNCTION = ' * '
    DISJUNCTION = ' + '

    def __init__(self, logic_value, unique_vars, result):
        self.vars = unique_vars
        self.result = result
        self.actions, self.operation_out_constituents = [self.CONJUNCTION,
                                                         self.DISJUNCTION]
        self.logic_value = logic_value
        self.CONSTANT_ONE = 1
        self.parts = sorted(self.logic_value.split(self.operation_out_constituents))
        self.result_value = self.reduced_func = self.logic_value

    def karnough_map(self, row, result, first_value, second_value, third_value):
        logic_value = row.value
        item = row.interpretation
        value = str(item[second_value]) + str(item[third_value])
        result[item[first_value] + 1][GREI_CODE[value]] = logic_value
        return result

    def create(self, *args):
        first_value = args[0]
        second_value = args[1]
        third_value = args[2]
        res = []
        for _ in range(3): res.append([0, 0, 0, 0, 0])
        action = self.actions
        res[1][0] = f'!{first_value}'
        res[2][0] = first_value
        res[0][1] = f'!{second_value}{action}!{third_value}'
        res[0][2] = f'!{second_value}{action}{third_value}'
        res[0][3] = f'{second_value}{action}{third_value}'
        res[0][4] = f'{second_value}{action}!{third_value}'
        truth_table = self.result
        for row in truth_table:
            res = self.karnough_map(row, res, first_value, second_value, third_value)
        return res

    @staticmethod
    def checking_items(values: list, existing: list) -> bool:
        return all(cell in existing for cell in values)

    def check_line(self, res, values, existing):
        for index, element in enumerate(res[1:], start=1):
            if element.count(self.CONSTANT_ONE) == 4:
                values.append([index])
                existing.extend([[index, col_ind] for col_ind in range(5)])
        return values, existing

    def check_figure(self, res, vertical_value, index, g_index, existing) -> bool:
        if index == 4: return False
        if vertical_value != self.CONSTANT_ONE: return False
        if res[g_index][index + 1] != self.CONSTANT_ONE: return False
        if g_index == 2 or res[g_index + 1][index] != self.CONSTANT_ONE: return False
        if res[g_index + 1][index + 1] != self.CONSTANT_ONE: return False
        cells = [[g_index, index], [g_index + 1, index + 1], [g_index + 1, index], [g_index, index + 1]]
        if self.checking_items(cells, existing): return False
        return True

    def figure_side(self, res, vertical, index, g_index, existing) -> bool:
        if g_index == 2: return False
        if index != 1 or vertical != self.CONSTANT_ONE: return False
        if res[g_index + 1][index] != self.CONSTANT_ONE: return False
        if res[g_index][4] != self.CONSTANT_ONE or res[g_index + 1][4] != self.CONSTANT_ONE: return False
        cells = [[g_index, index], [g_index + 1, index], [g_index, 4], [g_index + 1, 4]]
        if self.checking_items(cells, existing): return False
        return True

    @staticmethod
    def karno_figure(values, verticals, gorizontals, existing):
        values.append([verticals, verticals + 1, 0])
        existing.extend([
            [gorizontals, verticals],
            [gorizontals + 1, verticals + 1],
            [gorizontals + 1, verticals],
            [gorizontals, verticals + 1]])
        return values, existing

    @staticmethod
    def second_karno_figure(neighbor_indexes, col_ind, row_ind, founded):
        neighbor_indexes.append([col_ind, 4, 0])
        founded.extend([
            [row_ind, col_ind],
            [row_ind + 1, col_ind],
            [row_ind, 4],
            [row_ind + 1, 4]])
        return neighbor_indexes, founded

    def check_four_figure(self, res, values, existing):
        for index, element in enumerate(res):
            if index == 0:
                continue
            for col_ind, col_value in enumerate(element):
                if col_ind == 0:
                    continue
                if self.check_figure(res, col_value, col_ind, index, existing):
                    values, existing = self.karno_figure(values, col_ind, index,
                                                         existing)
                if self.figure_side(res, col_value, col_ind, index, existing):
                    values, existing = self.second_karno_figure(values, col_ind, index,
                                                                existing)
        return values, existing

    def two_line(self, res, neighbor_indexes, founded):
        for index, element in enumerate(res):
            if index == 0:
                continue
            for col_ind, col_value in enumerate(element):
                if col_ind == 0:
                    continue
                if index != 2 and col_value == self.CONSTANT_ONE and res[index + 1][col_ind] == self.CONSTANT_ONE and (
                        [index, col_ind] not in founded or [index + 1, col_ind] not in founded):
                    neighbor_indexes.append(
                        [index, index + 1, col_ind, col_ind]), \
                        founded.extend(
                            [
                                [index, col_ind],
                                [index + 1, col_ind]
                            ])
                elif col_ind != 4 and col_value == self.CONSTANT_ONE and res[index][
                    col_ind + 1] == self.CONSTANT_ONE and (
                        [index, col_ind] not in founded or [index, col_ind + 1] not in founded):
                    neighbor_indexes.append(
                        [index, index, col_ind, col_ind + 1]), \
                        founded.extend(
                            [
                                [index, col_ind],
                                [index, col_ind + 1]
                            ])
                elif col_ind == 1 and col_value == self.CONSTANT_ONE and element[-1] == self.CONSTANT_ONE and (
                        [index, 4] not in founded or [index, col_ind] not in founded):
                    neighbor_indexes.append(
                        [index,
                         index,
                         col_ind, -1]), \
                        founded.extend([
                            [index, col_ind],
                            [index, 4]])
        return neighbor_indexes, founded

    def one_line(self, res, values, existing):
        for index, element in enumerate(res):
            if index == 0:
                continue
            for column_index, column in enumerate(element):
                if column_index == 0:
                    continue
                if column == self.CONSTANT_ONE and [index, column_index] not in existing:
                    values, existing = self.processing_single_line(index, column_index, existing, values)
        return values, existing

    @staticmethod
    def processing_single_line(index, column_index, existing, values):
        values.append([index, column_index])
        existing.append([index, column_index])
        return values, existing

    def result(self, res):
        values = []
        existing = []
        values, existing = self.getting_result(res, values, existing)
        return self.sum(res, values)

    def getting_result(self, res, values, existing):
        values, existing = self.check_line(res, values, existing)
        values, existing = self.check_four_figure(res, values, existing)
        values, existing = self.two_line(res, values, existing)
        values, existing = self.one_line(res, values, existing)
        return values, existing

    def get_four(self, table, item):
        first_value = table[item[0]][0] + self.actions + table[0][item[2]]
        second_value = table[item[1]][0] + self.actions + table[0][item[3]]
        third_value = self.combine(first_value, second_value)
        return third_value

    def get_two(self, res, element, flag):
        value = f'{res[element[0]][0]}{self.actions}{res[0][element[1]]}'
        if flag: value = self.actions.join(
            [f'!{x}' if x.find('!') == -1 else x.replace('!', '') for x in value.split(self.actions)])
        return value

    @staticmethod
    def check_values(res, element, flag):
        value = res[element[0]][0]
        value = value.replace('!',
                              '') if '!' in value else f'!{value}' if flag else value if '!' in value else \
            value.replace(
                '!', '')
        return value

    def sum(self, res, indexes):
        values = []
        inversion = False
        for element in indexes:
            if len(element) == 1:
                value = self.check_values(res, element, inversion)
            elif len(element) == 2:
                value = self.get_two(res, element, inversion)
            elif len(element) == 3:
                value = self.combine(res[0][element[0]], res[0][element[1]])
            else:
                value = self.get_four(res, element)
            values.append(f'({value})')
        return values

    def combine(self, first_value, second_value):
        first_element, second_element = set(self.items(first_value)), set(self.items(second_value))
        result = first_element.intersection(second_element)
        flag = False
        if flag: result = [f'!{x}' if '!' not in x else x.replace('!', '') for x in result]
        return self.actions.join(result)

    def solution(self):
        res = self.create(*sorted(self.vars))
        indexes = []
        existing = []
        indexes, existing = self.proces_lines(res, indexes, existing)
        values = self.sum(res, indexes)
        values = [i for i in values if i]
        self.result_value = self.operation_out_constituents.join(values)

    def proces_lines(self, res, indexes, existing):
        indexes, existing = self.check_line(res, indexes, existing)
        indexes, existing = self.check_four_figure(res, indexes, existing)
        indexes, existing = self.two_line(res, indexes, existing)
        indexes, existing = self.one_line(res, indexes, existing)
        return indexes, existing

    def get_result(self):
        res = self.create(*sorted(self.vars))
        print(*res[0], sep='\t|\t', end='\n' + '_' * 80 + '\n')
        for index, element in enumerate(res[1:]):
            for item in element:
                print(str(item).center(8 + len(res[0][index + 1]), ' ') if item != element[0] else str(item).center(5,
                                                                                                                    ' '),
                      end=' ')
            print('\n' + '_' * 80, end='\n\n' if index != 1 else '\n')

    def common_elements(self, first_value: str, second_value: str):
        first_value = set(self.items(first_value))
        second_value = set(self.items(second_value))
        combination = first_value.union(second_value)
        combination = set(map(lambda x: x.replace('!', ''), combination))
        self.process_literals(combination, first_value, second_value)

    def process_literals(self, combination, first_value, second_value):
        if len(combination) == len(first_value):
            new_literals = first_value.intersection(second_value)
            if len(new_literals) != len(first_value) - 1:
                return None
            return self.actions.join(new_literals)

    def items(self, value: str):
        return [element for element in value.split(self.actions) if element]
