import math


def get_bin(x):
    return str(bin(x))[2:]


def complement(string, x):
    return "0" * (x - len(string)) + string


class TruthTableHandler:
    @staticmethod
    def permutation(n):
        vars_permutation = [[False] * n]
        while True:
            iter = n - 1
            current_permutation = vars_permutation[-1].copy()
            while iter >= 0:
                if not current_permutation[iter]:
                    break
                iter -= 1
            if iter < 0:
                break
            current_permutation[iter] = True
            iter += 1
            while iter < n:
                current_permutation[iter] = False
                iter += 1
            vars_permutation.append(current_permutation)
        return vars_permutation

    @staticmethod
    def another_permutation(n):
        print(n)
        print("another")
        unique_vars = int(math.log(n, 2))
        result = []
        value = 0
        for iteration in range(n):
            bin_value = get_bin(value)
            bin_value = complement(bin_value, unique_vars)
            additional_list = []
            for element in bin_value:
                if element != "0":
                    additional_list.append(True)
                else:
                    additional_list.append(False)
            result.append(additional_list)
            value += 1
        return result

    @staticmethod
    def print_truth_table(truth_table, variables, expression_result):
        for var in variables:
            print(f"{var}\t", end="")
        print("expr\tFi")
        for i in range(len(truth_table)):
            for j in range(len(truth_table[i])):
                print("1\t" if truth_table[i][j] else "0\t", end="")
            print("1\t" if expression_result[i] else "0\t", end="")
            print(i)
            print()
        print()

    @staticmethod
    def calculating_parts_PDNF(truth_table, variables, result):
        suitable_options = []
        function_parts = []
        for i in range(len(result)):
            if result[i]:
                suitable_options.append(truth_table[i])
        for i in range(len(suitable_options)):
            function_part = "("
            for j in range(len(variables)):
                if suitable_options[i][j]:
                    function_part += variables[j] + "*"
                else:
                    function_part += "(!" + variables[j] + ")*"
            function_part = function_part[:-1] + ")"
            function_parts.append(function_part)
        return function_parts

    @staticmethod
    def show_dpnf(truth_table, variables, expression_result):
        disjunction_result = ""
        parts = TruthTableHandler.calculating_parts_PDNF(truth_table, variables, expression_result)
        if len(parts) != 0:
            disjunction_result += parts[0]
            for i in range(1, len(parts)):
                disjunction_result += "+" + parts[i]
            print("Principal disjunction normal function:\n" + disjunction_result + "\n")
        else:
            print("Principal disjunction normal function doesn't exist\n")

    @staticmethod
    def get_dpnf(truth_table, variables, expression_result):
        disjunction_result = ""
        parts = TruthTableHandler.calculating_parts_PDNF(truth_table, variables, expression_result)
        if len(parts) != 0:
            disjunction_result += parts[0]
            for i in range(1, len(parts)):
                disjunction_result += "+" + parts[i]
        return disjunction_result

    @staticmethod
    def calculating_parts_of_pcnf(truth_table, variables, expression_result):
        suitable_options = []
        function_parts = []
        for i in range(len(expression_result)):
            if not expression_result[i]:
                suitable_options.append(truth_table[i])
        for i in range(len(suitable_options)):
            function_part = "("
            for j in range(len(variables)):
                if not suitable_options[i][j]:
                    function_part += variables[j] + "+"
                else:
                    function_part += "(!" + variables[j] + ")+"
            function_part = function_part[:-1] + ")"
            function_parts.append(function_part)
        return function_parts

    @staticmethod
    def print_pcnf(truth_table, variables, expression_result):
        disjunction = ""
        function_parts = TruthTableHandler.calculating_parts_of_pcnf(truth_table, variables, expression_result)
        if len(function_parts) != 0:
            disjunction += function_parts[0]
            for i in range(1, len(function_parts)):
                disjunction += "*" + function_parts[i]
            print("Principal conjuction normal function:\n" + disjunction + "\n")
        else:
            print("Principal conjuction normal function doesn't exist\n")

    @staticmethod
    def number_result_of_pdnf(truthTable, expressionResult):
        suitable_options = []
        results = []
        for i in range(len(expressionResult)):
            if expressionResult[i]:
                suitable_options.append(truthTable[i])
        for i in range(len(suitable_options)):
            binary_result = ""
            for j in range(len(suitable_options[i])):
                if suitable_options[i][j]:
                    binary_result += "1"
                else:
                    binary_result += "0"
            results.append(int(binary_result, 2))

    @staticmethod
    def number_result_of_pcnf(truth_table, result):
        suitable_options = []
        results = []
        for i in range(len(result)):
            if not result[i]:
                suitable_options.append(truth_table[i])
        for option in suitable_options:
            binary_result = ''.join(['0' if val else '1' for val in option])
            results.append(int(binary_result, 2))

    @staticmethod
    def from_binary_to_int(binary_value):
        result = 0
        for i in range(len(binary_value)):
            if binary_value[len(binary_value) - i - 1] == '1':
                result += 2 ** i
        return result

    @staticmethod
    def index(result):
        index = 0
        for i in range(len(result)):
            if result[i]:
                index += pow(2, len(result) - 1 - i)
        print("\nIndex Form:\ni = " + str(index))

    @staticmethod
    def show_pdnf(truth_table, variables, result):
        TruthTableHandler.show_dpnf(truth_table, variables, result)
        TruthTableHandler.number_result_of_pdnf(truth_table, result)

    @staticmethod
    def show_pcnf(truth_table, variables, result):
        TruthTableHandler.print_pcnf(truth_table, variables, result)
        TruthTableHandler.number_result_of_pcnf(truth_table, result)

    @staticmethod
    def final_result(truth_table, variables, result):
        TruthTableHandler.show_pdnf(truth_table, variables, result)
        print()
        TruthTableHandler.show_pcnf(truth_table, variables, result)
        TruthTableHandler.index(result)
