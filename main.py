from typing import List, Dict
from collections import deque
from solving.expression_handler import ExpressionHandler
from solving.truth_table import TruthTableHandler
from solving.logic_calculator import LogicCalculator
from solving.context import TruthTableRow
from solving.minimizing import Karnough


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
        min_ = Karnough(formula=logic_expression, mode="CNF", unique_vars=set(unique_variables), truth_table=res)
        min_.karnough_method()
        min_.print_karnough_table()
        print(min_.minimized_func)


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
    # main("(((!x1)*x2)+(x2->(!x3)))")
    main("((a->b)->c)")

