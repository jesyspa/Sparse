from SNode import SNode

def sparse(string):
    """Return a parse tree of string."""
    elts = string.replace('(', ' ( ').replace(')', ' ) ').split()
    return _sparse_impl(elts, 0)[0]

def sunparse(quote):
    """Return the given value as a string with an S-expression."""
    if isinstance(quote, SNode):
        quote = quote.value
    if isinstance(quote, tuple):
        return '(' + ' '.join([sunparse(e) for e in quote]) + ')'
    else:
        return str(quote)

def sprint(quote):
    """Print the given value as an S-expression."""
    print(sunparse(quote))

def _parse_atom(atom):
    """Return a type, value tuple for an atom."""
    try:
        val = int(atom)
        return SNode('num', val)
    except:
        return SNode('id', atom)

def _sparse_impl(elts, pos):
    """Return a parse tree and the position one past where it ended."""
    if elts[pos] != '(':
        return _parse_atom(elts[pos]), pos+1
    values = []
    pos += 1
    while elts[pos] != ')':
        value, tokens = _sparse_impl(elts, pos)
        values.append(value)
        pos = tokens
    return SNode('list', tuple(values)), pos+1


