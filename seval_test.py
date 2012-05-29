from nose.tools import eq_
from seval import seval
from SEnvironment import SEnvironment
import operator

builtins = SEnvironment()
builtins.define('+', lambda *args: sum(args))
builtins.define('*', operator.mul)
builtins.define('/', operator.floordiv)
builtins.define('%', operator.mod)
builtins.define('=', operator.eq)
builtins.define('<', operator.lt)
builtins.define('>', operator.gt)
builtins.define('<=', operator.le)
builtins.define('>=', operator.ge)

def seval_num_test():
    eq_(seval('3'), 3)

def seval_add_test():
    eq_(seval('(+ 3 2)', builtins), 5)

def seval_mul_test():
    eq_(seval('(* 3 2)', builtins), 6)

def seval_eq_test():
    eq_(seval('(= 1 1)', builtins), True)

def seval_if_test():
    eq_(seval('(if (= 1 1) 1 0)', builtins), 1)

def seval_env_test():
    env = SEnvironment()
    env.define('x', 5)
    eq_(seval('x', env), 5)

def seval_define_test():
    env = SEnvironment()
    seval('(define x 5)', env)
    eq_(env.lookup('x'), 5)

def seval_lambda_test():
    eq_(seval('((lambda () 5))'), 5)

def seval_lambda_with_args_test():
    eq_(seval('((lambda (x) x) 5)'), 5)

def seval_quote_test():
    eq_(seval('(quote (1 2 3))'), (1, 2, 3))

def seval_quote_quote_test():
    eq_(seval('(quote (quote (1 2 3)))'), ('quote', (1, 2, 3)))
