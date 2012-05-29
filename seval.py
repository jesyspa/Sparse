"""Provide functions for evaluation."""

from sparse import sparse
from SEnvironment import SEnvironment
from SNode import SNode
import operator


def seval(string, env=None):
    """Evaluate a string and return the result."""
    if env is None:
        env = SEnvironment()
    return _seval_impl(sparse(string), env)

def _if_impl(env, cond, true_case, false_case):
    """Evaluate and return true_case or false_case depending on cond."""
    if _seval_impl(cond, env):
        return _seval_impl(true_case, env)
    else:
        return _seval_impl(false_case, env)

def _define_impl(env, name, value):
    """Add the given name to the environment."""
    assert name.type == 'id', "Trying to define a non-identifier!"
    env.define(name.value, _seval_impl(value, env))

def _lambda_impl(env, params, *code):
    """Return an anonymous function taking params and evaluating code."""
    def impl(*args):
        assert len(params.value) == len(args), "Expected {} args, got {}.".format(
                len(params.value), len(args))
        inner_env = SEnvironment(env)
        for p, a in zip(params.value, args):
            assert p.type == 'id', "Trying to use a non-identifier as a parameter name!"
            inner_env.define(p.value, a)
        for c in code[:-1]:
            _seval_impl(c, inner_env)
        return _seval_impl(code[-1], inner_env)
    return impl

SPECIAL_FORMS = {
    'if': _if_impl, 
    'define': _define_impl,
    'lambda': _lambda_impl,
        }

def _seval_impl(tree, env):
    """Evaluate the given parse tree."""
    if tree.type == 'num':
        return tree.value
    if tree.type == 'id':
        return env.lookup(tree.value)
    if tree.type == 'list':
        func = tree.value[0]
        if func.value in SPECIAL_FORMS:
            args = tree.value[1:]
            return SPECIAL_FORMS[func.value](env, *args)
        args = [_seval_impl(subtree, env) for subtree in tree.value[1:]]
        return _seval_impl(func, env)(*args)
