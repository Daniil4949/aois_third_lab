class TestExpressions:
    testExpressions = [
        "!(((!x1)+(!x2))*(!((!x2)*(!x3))))",
        "(p*(q+r))",
        "((P==Q)==R)",
        "(!(P->(P->(Q==Q))))",
        "((P->Q)+(P->(Q*P)))",
        "((Q+(R*(!P)))->(P==R))",
        "(((!P)->(Q*R))==((!(!(P+Q)))->S))",
        "((P->Q)->((P->(Q->R))->(P->R)))",
        "(!((S->((!R)+(P*Q)))==(P*(!(Q->R))))))",
        "((((P->R)*(Q->S))*((!P)+(!S)))->((!P)+(!Q)))"
    ]

    @staticmethod
    def get_test_expressions():
        return TestExpressions.testExpressions
