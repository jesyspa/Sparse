"""Provide functions for evaluation."""

from sparse import sparse, sunparse, sprint
from SEnvironment import SEnvironment
from SException import SException

def seval(string, env=None):
    """Evaluate a string and return the result."""
    if env is None:
        env = SEnvironment()
    return seval_tree(sparse(string), env)

def seval_strip(string, env=None):
    return _strip_annotations(seval(string, env))

def _strip_annotations(tree):
    if tree.type == 'list':
        return tuple(_strip_annotations(e) for e in tree.value)
    return tree.value


def seval_tree(tree, env):
    """Evaluate the given parse tree."""
    if tree.type == 'id':
        return env.lookup(tree.value)
    if tree.type == 'list':
        if not tree.value:
            raise SException("Attempting to evaluate empty list.")
        if tree.value[0].type == 'sf':
            if len(tree.value) == 1:
                raise SException("Trying to evaluate pure magic.")
            args = tree.value[2:]
            func = seval_tree(tree.value[1], env)
        else:
            args = [seval_tree(subtree, env) for subtree in tree.value[1:]]
            func = seval_tree(tree.value[0], env)
        if func.type != 'function':
            raise SException("Attempting to call non-function.")
        return func.value(env, *args)
    else:
        return tree

