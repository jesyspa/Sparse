from SEnvironment import SEnvironment
from SException import SException
from SNode import SNode
from seval import seval, seval_tree
from sparse import sprint
import operator


def _if(env, *args):
    """Evaluate and return true_case or false_case depending on cond."""
    if len(args) != 3:
        raise SException("if takes 3 parameters ({} given).".format(len(args)))
    cond, true_case, false_case = args
    if seval_tree(cond, env).value:
        return seval_tree(true_case, env)
    else:
        return seval_tree(false_case, env)

def _define(env, *args):
    """Add the given name to the environment."""
    if len(args) != 2:
        raise SException("define takes 2 parameters ({} given).".format(len(args)))
    name, value = args
    if name.type != 'id':
        raise SException("Trying to define a non-identifier!")
    env.define(name.value, seval_tree(value, env))
    return SNode('none', None)

def _lambda(env, *args):
    """Return an anonymous function taking params and evaluating code."""
    if not args:
        raise SException("Malformed lambda.")
    params, *code = args
    if params.type != 'list':
        raise SException("Parameters must be given as a list.")
    restargs = params.value and params.value[0].type == 'list'
    nameargs = params.value[0] if restargs else params
    if not code:
        raise SException("Function defined with no body.")
    def impl(dummy_env, *args):
        if not restargs and len(params.value) != len(args):
            raise SException("Expected {} args, got {}.".format(len(params.value), len(args)))
        NON_SYMBOL_ERROR = "Trying to use a non-symbol as a parameter name!"
        inner_env = SEnvironment(env)
        for p, a in zip(nameargs.value, args):
            if p.type != 'id':
                raise SException(NON_SYMBOL_ERROR)
            inner_env.define(p.value, a)
        if restargs:
            if params.value[1].type != 'id':
                raise SException(NON_SYMBOL_ERROR)
            rest = SNode('list', args[len(nameargs.value):])
            inner_env.define(params.value[1].value, rest)
        for c in code[:-1]:
            seval_tree(c, inner_env)
        return seval_tree(code[-1], inner_env)
    return SNode('function', impl)

def _quote(env, elt):
    """Return the quoted object verbatim."""
    return elt

def _quasiquote(env, elt):
    """Return the quoted expression, unquoting unquotes."""
    if elt.type != 'list':
        return elt
    if (len(elt.value) > 0 and elt.value[0].type == 'id'
            and elt.value[0].value == 'unquote'):
        return seval_tree(elt.value[1], env)
    result = []
    for e in elt.value:
        if (e.type != 'list' or not e.value
                or e.value[0].value != 'unquote-splice'):
            result.append(_quasiquote(env, e))
        else:
            result.extend(seval_tree(e.value[1], env).value)
    return SNode('list', tuple(result))

def _cons(env, elt, li):
    if li.type != 'list':
        raise SException("Trying to concatenate with non-list.")
    return SNode('list', (elt,) + li.value)

def _eval(real_env, expr, env):
    if env.type != 'env':
        raise SException("Passed in value is not an environment.")
    return seval_tree(expr, env.value)

def _apply(env, f, args):
    if f.type != 'function':
        raise SException("Attempting to apply a non-function.")
    if args.type != 'list':
        raise SException("Attempting to apply on non-list.")
    return f.value(env, *args.value)

def _print(env, quote):
    sprint(quote)
    return SNode('none', None)

def _append(env, *lists):
    result = tuple()
    for li in lists:
        if li.type != 'list':
            raise SException("Attempting to append a non-list.")
        result += li.value
    return SNode('list', result)

def _make_func(func):
    def impl(env, *args):
        try:
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
                raise SException("Unexpected return type of function: {}".format(type(value)))
        except TypeError as e:
            raise SException(str(e))
    return SNode('function', impl)

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
    builtins.define('print', SNode('function', _print))
    builtins.define('apply', SNode('function', _apply))
    builtins.define('list', _make_func(lambda *args: args))
    builtins.define('append', SNode('function', _append))
    builtins.define('cons', SNode('function', _cons))
    builtins.define('head', _make_func(lambda x: x[0]))
    builtins.define('tail', _make_func(lambda x: x[1:]))
    builtins.define('this-env', SNode('function', lambda env: SNode('env', env)))
    builtins.define('parent', SNode('function', lambda env, e: SNode('env',
        e.value.parent)))
    builtins.define('eval', SNode('function', _eval))
    builtins.define('nil', SNode('list', tuple()))
    builtins.define('#t', SNode('bool', True))
    builtins.define('#f', SNode('bool', False))
    builtins.define('if', SNode('function', _if))
    builtins.define('lambda', SNode('function', _lambda))
    builtins.define('define', SNode('function', _define))
    builtins.define('quote', SNode('function', _quote))
    builtins.define('quasiquote', SNode('function', _quasiquote))
    seval("""
        (~define defmacro
          (~lambda (name args . body)
            (eval `(~define ,name
                     (~lambda ,args
                       (eval ((~lambda () ,@body))
                             (parent (this-env)))))
                   (parent (this-env)))))
    """, builtins)
    seval("""
        (~defmacro defun (name args . body)
          `(~define ,name
            (~lambda ,args ,@body)))
    """, builtins)
    seval("""
        (~defmacro begin (. body)
          `((lambda () ,@body)))
    """, builtins)
    return builtins

