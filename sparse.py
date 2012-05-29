from SNode import SNode

def sparse(string):
    """Return a parse tree of string."""
    elts = string.replace('(', ' ( ').replace(')', ' ) ').split()
    return _sparse_impl(elts, 0)[0]

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


