from typing import List


class TruthTableRow:
    def __init__(self, interpretation: dict, value: int):
        self.interpretation = interpretation
        self.value = value


class Context:

    def __int__(self, truth_table):
        self.truth_table = truth_table
