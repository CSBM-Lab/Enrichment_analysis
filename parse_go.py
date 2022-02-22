from goatools import obo_parser

term = obo_parser.GODag('go.obo').query_term('GO:0045259')
print(term.parents)
print(term.level)
print(term.depth)
print(term.name)
