from logic_formula_scripts.logical_formula_solver import TruthTableSolver,  FullLogicalResult
from logic_formula_scripts.fcnf_fdnf_converter import create_conjunction, create_disjunction


formula: str = '!((a+!b)&!(a&!c))'


def main():
    formula_solver = TruthTableSolver(formula)
    formula_solver.present_result_table()
    truth_table: list[FullLogicalResult] = TruthTableSolver(formula).solve_formula()
    conjunction, conjunction_num_form = create_conjunction(truth_table)
    disjunction, disjunction_num_form = create_disjunction(truth_table)
    truth_table_values = [implementation.formula_value for implementation in truth_table]
    formula_vector = int(''.join([str(value) for value in truth_table_values]), 2)
    print(f'Совершенная конъюктивная нормальна форма: {conjunction}\n'
          f'Совершенная конъюктивная нормальная форма - численное представление: {conjunction_num_form}\n'
          f'Совершенная дизъюнктивная нормальная форма: {disjunction}\n'
          f'Совершенная дизъюнктивная нормальная форма - численное представление: {disjunction_num_form}\n'
          f'Вектор формулы: {formula_vector}')


if __name__ == "__main__":
    main()
