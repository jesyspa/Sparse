from SEnvironment import SEnvironment
from SNode import SNode
from seval import seval_tree
import operator


def _if_impl(env, menv, cond, true_case, false_case):
    """Evaluate and return true_case or false_case depending on cond."""
    if seval_tree(cond, env, menv):
        return seval_tree(true_case, env, menv)
    else:
        return seval_tree(false_case, env, menv)

def _define_impl(env, menv, name, value):
    """Add the given name to the environment."""
    assert name.type == 'id', "Trying to define a non-identifier!"
    env.define(name.value, seval_tree(value, env, menv))

def _lambda_impl(env, menv, params, *code):
    """Return an anonymous function taking params and evaluating code."""
    def impl(*args):
        assert len(params.value) == len(args), "Expected {} args, got {}.".format(
                len(params.value), len(args))
        inner_env = SEnvironment(env)
        for p, a in zip(params.value, args):
            assert p.type == 'id', "Trying to use a non-identifier as a parameter name!"
            inner_env.define(p.value, a)
        for c in code[:-1]:
            seval_tree(c, inner_env, menv)
        return seval_tree(code[-1], inner_env, menv)
    return impl

def _quote_impl(env, menv, elt):
    """Return the quoted object verbatim."""
    if elt.type != 'list':
        return elt.value
    return tuple(_quote_impl(env, menv, e) for e in elt.value)

def make_stdenv():
    """Return an env, menv pair."""
    normal_names = SEnvironment()
    normal_names.define('+', lambda *args: sum(args))
    normal_names.define('-', operator.sub)
    normal_names.define('*', operator.mul)
    normal_names.define('/', operator.floordiv)
    normal_names.define('%', operator.mod)
    normal_names.define('=', operator.eq)
    normal_names.define('/=', operator.ne)
    normal_names.define('<', operator.lt)
    normal_names.define('>', operator.gt)
    normal_names.define('<=', operator.le)
    normal_names.define('>=', operator.ge)
    normal_names.define('1-', lambda x: x+1)
    normal_names.define('1+', lambda x: x-1)
    normal_names.define('not', operator.not_)
    normal_names.define('read-int', lambda: int(input('')))
    normal_names.define('print', lambda x: sprint(x))
    normal_names.define('apply', lambda f, args: f(*args))
    normal_names.define('list', lambda *args: args)
    normal_names.define('cons', lambda x, y: [x] + y)
    normal_names.define('head', lambda x: x[0])
    normal_names.define('tail', lambda x: x[1:])
    normal_names.define('nil', tuple())
    normal_names.define('#t', True)
    normal_names.define('#f', False)

    special_forms = SEnvironment()
    special_forms.define('if', _if_impl)
    special_forms.define('lambda', _lambda_impl)
    special_forms.define('define', _define_impl)
    special_forms.define('quote', _quote_impl)
    return normal_names, special_forms

