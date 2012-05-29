"""Provide functions for evaluation."""

from sparse import sparse
from SEnvironment import SEnvironment

def seval(string, env=None, menv=None):
    """Evaluate a string and return the result."""
    if env is None:
        env = SEnvironment()
    if menv is None:
        menv = SEnvironment()
    return seval_tree(sparse(string), env, menv)


def seval_tree(tree, env, menv):
    """Evaluate the given parse tree."""
    if tree.type == 'num':
        return tree.value
    if tree.type == 'id':
        return env.lookup(tree.value)
    if tree.type == 'list':
        func = tree.value[0]
        if func.value in menv:
            args = tree.value[1:]
            return menv.lookup(func.value)(env, menv, *args)
        args = [seval_tree(subtree, env, menv) for subtree in tree.value[1:]]
        return seval_tree(func, env, menv)(*args)

