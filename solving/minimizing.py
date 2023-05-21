from itertools import combinations
from functools import reduce
from typing import List


def combine(logical_value: List[List[str]]) -> List[List[str]]:
    normal_form: List[List[str]] = []
    for i in range(len(logical_value)):
        for j in range(i + 1, len(logical_value)):
            first_value, second_value = set(logical_value[i]), set(logical_value[j])
            value = sorted(list(first_value.intersection(second_value)),
                           key=lambda x: x[-1])
            if len(value) == 2: normal_form.append(value)
    return normal_form


def calculation_method(function):
    min_ = function[:]
    for element in min_:
        mnf_copy = min_[:]
        mnf_copy.remove(element)
    return min_


def fill_calc_tabl_method(res, min_, normal_form):
    colls = [False] * len(res[0])
    for i in range(len(res[0])):
        verifiable_column = [j[i] for j in res]
        if verifiable_column.count(True) == 1:
            val = normal_form[verifiable_column.index(True)]
            if val not in min_:
                min_.append(val)
            colls = [a or b for a, b in zip(colls, res[verifiable_column.index(True)])]
    return colls, min_


def calc_tabl(res_tabl, values, normal_form, colls):
    min_amount = float('inf')
    res = []
    for element in range(1, len(values) + 1):
        for subset in combinations(values, element):
            set_of_verifiable_implicants = [res_tabl[normal_form.index(i)] for i in subset]
            set_of_verifiable_implicants = reduce(lambda x, y: [i or j for i, j in zip(x, y)],
                                                  set_of_verifiable_implicants)
            if all(x[0] or x[1] for x in zip(set_of_verifiable_implicants, colls)) and len(
                    set_of_verifiable_implicants) < min_amount:
                min_amount = len(set_of_verifiable_implicants)
                res = subset
    return res


def calc_tabl_function(normal_form, value):
    result = []
    tabl_res = [[len(set(i) & set(j)) == 2 for j in value] for i in normal_form]
    col, result = fill_calc_tabl_method(tabl_res, result, normal_form)
    values = [i for i in normal_form if i not in result]
    if False in col:
        subset = calc_tabl(tabl_res, values, normal_form, col)
        result.extend(subset)
    print_calculation_tabular_table(value, tabl_res, normal_form)
    return result


def print_calculation_tabular_table(formula, table, normal_form):
    print("        ", end="")
    for i in formula:
        flag = "*"
        print(f"| {flag.join(i).ljust(10)} ", end="")
    print()
    for index, i in enumerate(table):
        print(f" {flag.join(normal_form[index]).rjust(6)} ", end="")
        for j in i:
            if j:
                print("|     x     ", end="")
            else:
                print("|           ", end="")
        print()


def get_final_result(logical_value):
    result = '+'.join(['*'.join(element) for element in logical_value])
    print(f"minimized DNF: {result}")


def solve(formula):
    formula = [i.split("*") for i in formula.split(" + ")]
    dnf = combine(formula)
    print("Calculation method:")
    result = calculation_method(dnf)
    get_final_result(result)
    print("Calculation-tabular method:")
    result = calc_tabl_function(dnf, formula)
    get_final_result(result)
