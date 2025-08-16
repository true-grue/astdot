import astdot


def test():
    output = r'''
digraph {
0 [label="Module"]
1 [label="list"]
2 [label="Expr"]
3 [label="BinOp"]
4 [label="Constant\nvalue: 2"]
5 [label="Add"]
6 [label="Constant\nvalue: 2"]
0 -> 1 [label=".body"]
1 -> 2 [label="[0]"]
2 -> 3 [label=".value"]
3 -> 4 [label=".left"]
3 -> 5 [label=".op"]
3 -> 6 [label=".right"]
}
    '''
    assert astdot.source_to_dot('2 + 2', style='').strip() == output.strip()
