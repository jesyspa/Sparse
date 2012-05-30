from SNode import SNode

def sparse(string):
    """Return a parse tree of string."""
    lexer = make_lexer()
    parser = make_parser()
    return parser.parse(string)

def sunparse(tree):
    """Return the given value as a string with an S-expression."""
    if tree.type != 'list':
        return str(tree.value)
    elif len(tree.value) > 0 and tree.value[0].type == 'list':
        inner = ' '.join([sunparse(e) for e in tree.value[0].value])
        this = ' '.join([sunparse(e) for e in tree.value[1:]])
        return '(' + inner + ' . ' + this + ')'
    else:
        return '(' + ' '.join([sunparse(e) for e in tree.value]) + ')'

def sprint(quote):
    """Print the given value as an S-expression."""
    print(sunparse(quote))

from ply import lex, yacc

tokens = (
    'LPAREN',
    'RPAREN',
    'TILDE',
    'QUOTE',
    'QQUOTE',
    'COMMA',
    'DOT',
    'SYMBOL',
    'NUMBER',
)

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_TILDE = '~'
t_QUOTE = "'"
t_QQUOTE = '`'
t_COMMA = ','
t_DOT = r'\.'
t_SYMBOL = r'[a-zA-Z\-_?!+/*%=<>][a-zA-Z0-9\-_?!+/*%=<>]*'
t_NUMBER = r'[0-9]+'
t_ignore_COMMENT = r';.*'
t_ignore = ' \t\n'

def t_error(t):
    print("Illegal character {}.".format(t.value[0]))
    t.lexer.skip(1)

def make_lexer(*args, **kwargs):
    return lex.lex(*args, **kwargs)

def p_expr_from_number(p):
    "expr : NUMBER"
    p[0] = SNode('num', int(p[1]))

def p_expr_from_symbol(p):
    "expr : SYMBOL"
    p[0] = SNode('id', p[1])

def p_tilde_expr(p):
    "expr : TILDE"
    p[0] = SNode('sf', '~')

def p_quoted_expr(p):
    "expr : QUOTE expr"
    p[0] =  SNode('list', (SNode('sf', '~'), SNode('id', 'quote'), p[2]))

def p_quasiquoted_expr(p):
    "expr : QQUOTE expr"
    p[0] =  SNode('list', (SNode('sf', '~'), SNode('id', 'quasiquote'), p[2]))

def p_unquoted_expr(p):
    "expr : COMMA expr"
    p[0] = SNode('list', (SNode('id', 'unquote'), p[2]))

def p_expr_from_list(p):
    "expr : LPAREN list RPAREN"
    p[0] = p[2]

def p_list_with_dot(p):
    "list : list DOT rhslist"
    p[0] = SNode('list', (p[1],) + p[3])

def p_list_to_rhslist(p):
    "list : rhslist"
    p[0] = SNode('list', p[1])

def p_rhslist_with_elem(p):
    "rhslist : rhslist expr"
    p[0] = p[1] + (p[2],)

def p_listpart_to_empty(p):
    "rhslist : "
    p[0] = tuple()

def make_parser(*args, **kwargs):
    make_lexer()
    return yacc.yacc(debug=1)

