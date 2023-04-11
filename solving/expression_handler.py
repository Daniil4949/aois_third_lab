class ExpressionHandler:
    @staticmethod
    def counting_variables_of_expression(expression, variables, all_values):
        for i in range(len(expression)):
            if expression[i].isalpha():
                var = 1
                while i + var < len(expression) and expression[i + var].isdigit():
                    var += 1
                if expression[i:i + var] not in variables:
                    variables.append(expression[i:i + var])
                all_values.append(expression[i:i + var])

    @staticmethod
    def dividing_on_tokens(expression, tokens, all_variables):
        variable = 0
        i = 0
        while i < len(expression):
            if expression[i].isalpha():
                tokens.append(all_variables[variable])
                i += (len(all_variables[variable]) - 1)
                variable += 1
            elif expression[i] != ' ':
                if (expression[i] == '-' and expression[i + 1] == '>') or (
                        expression[i] == '=' and expression[i + 1] == '='):
                    tokens.append(expression[i:i + 2])
                    i += 1
                else:
                    tokens.append(expression[i])
            i += 1

    @staticmethod
    def comparing_number_of_brackets(expression):
        try:
            opening_brackets = expression.count("(")
            closing_brackets = expression.count(")")
            if opening_brackets == closing_brackets:
                return True
            elif opening_brackets > closing_brackets:
                raise Exception("Incorrect. Symbol ')' is necessary here")
            else:
                raise Exception("Incorrect. Symbol ')' is not necessary here")
        except Exception as ex:
            print(ex)
            return False

    @staticmethod
    def checking_variables(variable):
        try:
            if len(variable) > 1 and variable[1] == '0':
                raise Exception(f"Incorrect - \"{variable}\"")
            for i in range(1, len(variable)):
                if not variable[i].isdigit():
                    raise Exception(f"Incorrect - \"{variable}\"")
            return True
        except Exception as ex:
            print(ex)
            return False

    @staticmethod
    def check(token, unique_values):
        signs = ["!", "+", "*", "->", "==", ")", "("]
        try:
            if token in unique_values:
                return ExpressionHandler.checking_variables(token)
            elif token in signs:
                return True
            else:
                raise Exception(f"Unknown symbol \"{token}\"")
        except Exception as ex:
            print(ex)
            return False

    @staticmethod
    def tokens_check(tokens, unique_values):
        try:
            for i in range(len(tokens) - 1):
                if tokens[i] in unique_values and tokens[i + 1] in unique_values:
                    raise Exception("Incorrect value")
        except Exception as ex:
            print(ex)
            return False
        return True

    @staticmethod
    def expression_correct(expression, tokens, unique_values):
        if len(unique_values) == 0:
            print("I do not see any variables here...")
            return False
        for token in tokens:
            if not ExpressionHandler.check(token, unique_values):
                return False
        return ExpressionHandler.comparing_number_of_brackets(expression) and ExpressionHandler.tokens_check(tokens,
                                                                                                             unique_values)
