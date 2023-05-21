from typing import List, Dict
from collections import deque
from solving.expression_handler import ExpressionHandler
from solving.truth_table import TruthTableHandler
from solving.logic_calculator import LogicCalculator
from solving.context import TruthTableRow
from solving.minimizing_karno import Karnough
from solving.utils import translate_dpnf
from solving.minimizing import solve


def main(logic_expression):
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
        TruthTableHandler.print_truth_table(truth_table, unique_variables, result_of_expression)
        TruthTableHandler.final_result(truth_table, unique_variables, result_of_expression)
        res: list = []
        for element in range(len(result_of_expression)):
            interpretation = dict()
            for i in range(len(unique_variables)):
                interpretation[unique_variables[i]] = int(truth_table[element][i])
            x = TruthTableRow(value=int(result_of_expression[element]), interpretation=interpretation)
            res.append(x)
        res_ = TruthTableHandler.get_dpnf(truth_table, unique_variables, result_of_expression)
        min_ = Karnough(logic_value=logic_expression, unique_vars=set(unique_variables), result=res)
        min_.solution()
        min_.get_result()
        print(min_.result_value)
        res_ = translate_dpnf(res_)
        solve(res_)


def to_truth(result_of_expression, unique_variables, truth_table):
    res: list = []
    for element in range(len(result_of_expression)):
        interpretation = dict()
        for i in range(len(unique_variables)):
            interpretation[unique_variables[i]] = int(truth_table[element][i])
        x = TruthTableRow(value=int(result_of_expression[element]), interpretation=interpretation)
        res.append(x)
    return res


if __name__ == "__main__":
    main("((a+b)*(!c))")
