from SEnvironment import SEnvironment
from SNode import SNode
from seval import seval_tree
import operator


def _if(env, cond, true_case, false_case):
    """Evaluate and return true_case or false_case depending on cond."""
    if seval_tree(cond, env).value:
        return seval_tree(true_case, env)
    else:
        return seval_tree(false_case, env)

def _define(env, name, value):
    """Add the given name to the environment."""
    assert name.type == 'id', "Trying to define a non-identifier!"
    env.define(name.value, seval_tree(value, env))
    return SNode('none', None)

def _lambda(env, params, *code):
    """Return an anonymous function taking params and evaluating code."""
    def impl(dummy_env, *args):
        assert len(params.value) == len(args), "Expected {} args, got {}.".format(
                len(params.value), len(args))
        inner_env = SEnvironment(env)
        for p, a in zip(params.value, args):
            assert p.type == 'id', "Trying to use a non-symbol as a parameter name!"
            inner_env.define(p.value, a)
        for c in code[:-1]:
            seval_tree(c, inner_env)
        return seval_tree(code[-1], inner_env)
    return SNode('function', impl)

def _quote(env, elt):
    """Return the quoted object verbatim."""
    if elt.type != 'list':
        return elt
    return SNode('list', tuple(_quote(env, e) for e in elt.value))

def _make_func(func):
    def impl(env, *args):
        value = func(*(a.value for a in args))
        if isinstance(value, str):
            return SNode('id', value)
        elif isinstance(value, list):
            return SNode('list', value)
        elif isinstance(value, tuple):
            return SNode('list', tuple(value))
        elif isinstance(value, int):
            return SNode('num', value)
        elif isinstance(value, bool):
            return SNode('bool', value)
        elif isinstance(value, SNode):
            return value
        elif value is None:
            return SNode('none', None)
        else:
            raise Exception("Unexpected return type of function: {}".format(type(value)))
    return SNode('function', impl)

def _cons(env, elt, li):
    assert li.type == 'list', "Trying to concatenate with non-list."
    return SNode('list', (elt,) + li.value)

def make_stdenv():
    """Return an SEnvironment with builtins."""
    builtins = SEnvironment()
    builtins.define('+', _make_func(lambda *args: sum(args)))
    builtins.define('-', _make_func(operator.sub))
    builtins.define('*', _make_func(operator.mul))
    builtins.define('/', _make_func(operator.floordiv))
    builtins.define('%', _make_func(operator.mod))
    builtins.define('=', _make_func(operator.eq))
    builtins.define('/=', _make_func(operator.ne))
    builtins.define('<', _make_func(operator.lt))
    builtins.define('>', _make_func(operator.gt))
    builtins.define('<=', _make_func(operator.le))
    builtins.define('>=', _make_func(operator.ge))
    builtins.define('1-', _make_func(lambda x: x+1))
    builtins.define('1+', _make_func(lambda x: x-1))
    builtins.define('not', _make_func(operator.not_))
    builtins.define('read-int', _make_func(lambda: int(input(''))))
    builtins.define('print', _make_func(lambda x: sprint(x)))
    builtins.define('apply', _make_func(lambda f, args: f(*args)))
    builtins.define('list', _make_func(lambda *args: args))
    builtins.define('cons', SNode('function', _cons))
    builtins.define('head', _make_func(lambda x: x[0]))
    builtins.define('tail', _make_func(lambda x: x[1:]))
    builtins.define('nil', SNode('list', tuple()))
    builtins.define('#t', SNode('bool', True))
    builtins.define('#f', SNode('bool', False))
    builtins.define('if', SNode('function', _if))
    builtins.define('lambda', SNode('function', _lambda))
    builtins.define('define', SNode('function', _define))
    builtins.define('quote', SNode('function', _quote))
    return builtins

