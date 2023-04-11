class LogicCalculator:
    @staticmethod
    def calculating(tokens, variables, values, stack_elements, stack_variables):
        signs = ["!", "*", "+", "->", "=="]
        for token in tokens:
            if token in variables:
                stack_variables.append(values[token])
            elif token in signs:
                while len(stack_elements) >= 1 and Priority.get_priority(stack_elements[-1]) >= Priority.get_priority(
                        token):
                    stack_variables.append(LogicCalculator.execute_operation(stack_variables, stack_elements.pop()))
                stack_elements.append(token)
            else:
                if token == "(":
                    stack_elements.append(token)
                else:
                    while stack_elements[-1] != "(":
                        stack_variables.append(LogicCalculator.execute_operation(stack_variables, stack_elements.pop()))
                    stack_elements.pop()
        while len(stack_elements) != 0:
            stack_variables.append(LogicCalculator.execute_operation(stack_variables, stack_elements.pop()))
        return stack_variables.pop()

    @staticmethod
    def binary_operation(stack_variables, sign):
        second_value = stack_variables.pop()
        first_value = stack_variables.pop()
        if sign == "*":
            return LogicCalculator.conjunction(first_value, second_value)
        elif sign == "+":
            return LogicCalculator.disjunction(first_value, second_value)
        elif sign == "->":
            return LogicCalculator.implication(first_value, second_value)
        else:
            return LogicCalculator.equivalence(first_value, second_value)

    @staticmethod
    def execute_operation(stack_variables, sign):
        if sign == "!":
            return LogicCalculator.inversion(stack_variables.pop())
        else:
            return LogicCalculator.binary_operation(stack_variables, sign)

    @staticmethod
    def conjunction(x1, x2):
        return x1 and x2

    @staticmethod
    def disjunction(x1, x2):
        return x1 or x2

    @staticmethod
    def inversion(x1: bool) -> bool:
        return not x1

    @staticmethod
    def implication(x1, x2):
        return not (x1 and not x2)

    @staticmethod
    def equivalence(x1: bool, x2: bool) -> bool:
        return x1 == x2


class Priority:
    priorities = {
        "!": 5,
        "*": 4,
        "+": 3,
        "->": 2,
        "==": 1
    }

    @staticmethod
    def get_priority(sign):
        if sign in Priority.priorities:
            return Priority.priorities[sign]
        else:
            return 0
