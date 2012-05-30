"""Provide functions for evaluation."""

from sparse import sparse, sunparse
from SEnvironment import SEnvironment

def seval(string, env=None):
    """Evaluate a string and return the result."""
    if env is None:
        env = SEnvironment()
    tree = seval_tree(sparse(string), env)
    print(tree)
    return _strip_annotation(tree)

def _strip_annotation(tree):
    if tree.type == 'list':
        return tuple(_strip_annotation(e) for e in tree.value)
    return tree.value


def seval_tree(tree, env):
    """Evaluate the given parse tree."""
    if tree.type == 'id':
        return env.lookup(tree.value)
    if tree.type == 'list':
        if tree.value[0].type == 'sf':
            args = tree.value[2:]
            func = seval_tree(tree.value[1], env)
        else:
            args = [seval_tree(subtree, env) for subtree in tree.value[1:]]
            func = seval_tree(tree.value[0], env)
        assert func.type == 'function', "Attempting to call non-function."
        return func.value(env, *args)
    else:
        return tree

