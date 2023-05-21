def translate_dpnf(formula: str):
    formula = formula.replace("(", "")
    formula = formula.replace(")", "")
    formula = " + ".join(formula.split("+"))
    return formula
