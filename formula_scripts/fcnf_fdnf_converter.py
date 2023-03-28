def create_conjunction(truth_table):
    conjunction_implementation_numbers: list[str] = []
    implementation_number: int = 0
    disjunction_sets: list[str] = []
    for element in truth_table:
        if element.formula_value == 0:
            disjunction_set: list[str] = []
            conjunction_implementation_numbers.append(str(implementation_number))
            for var, value in element.logical_interpretation.items():
                if value == 0:
                    disjunction_set.append(var)
                else:
                    disjunction_set.append('!' + var)
            disjunction_sets.append('(' + ' ∨ '.join(disjunction_set) + ')')
        implementation_number += 1
    conjunction_string = ' ∧ '.join(disjunction_sets)
    conjunction_num_form = '∧(' + ', '.join(conjunction_implementation_numbers) + ')'
    return conjunction_string, conjunction_num_form


def create_disjunction(truth_table):
    disjunction_implementation_numbers: list[str] = []
    implementation_number = 0
    conjunction_sets: list[str] = []
    for implementation in truth_table:
        if implementation.formula_value == 1:
            conjunction_set: list[str] = []
            disjunction_implementation_numbers.append(str(implementation_number))
            for var, value in implementation.logical_interpretation.items():
                if value == 1:
                    conjunction_set.append(var)
                else:
                    conjunction_set.append('!' + var)
            conjunction_sets.append('(' + ' ∧ '.join(conjunction_set) + ')')
        implementation_number += 1
    disjunction_string = ' ∨ '.join(conjunction_sets)
    disjunction_num_form = '∨(' + ', '.join(disjunction_implementation_numbers) + ')'
    return disjunction_string, disjunction_num_form
