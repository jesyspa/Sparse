from SNode import SNode

def sparse(string):
    """Return a parse tree of string."""
    elts = (string.replace('(', ' ( ')
                  .replace(')', ' ) ')
                  .replace("'", " ' ")
                  .replace("~", " ~ ")
                  .split())
    return _sparse_impl(elts, 0)[0]

def sunparse(tree):
    """Return the given value as a string with an S-expression."""
    if tree.type == 'list':
        return '(' + ' '.join([sunparse(e) for e in tree.value]) + ')'
    else:
        return str(tree.value)

def sprint(quote):
    """Print the given value as an S-expression."""
    print(sunparse(quote))

def _parse_atom(atom):
    """Return a type, value tuple for an atom."""
    if atom == '~':
        return SNode('sf', '~')
    try:
        val = int(atom)
        return SNode('num', val)
    except:
        return SNode('id', atom)

def _sparse_impl(elts, pos):
    """Return a parse tree and the position one past where it ended."""
    if elts[pos] == "'":
        rest, pos = _sparse_impl(elts, pos+1)
        return SNode('list', (SNode('sf', '~'), SNode('id', 'quote'), rest)), pos
    elif elts[pos] != '(':
        return _parse_atom(elts[pos]), pos+1
    values = []
    pos += 1
    while elts[pos] != ')':
        value, tokens = _sparse_impl(elts, pos)
        values.append(value)
        pos = tokens
    return SNode('list', tuple(values)), pos+1


