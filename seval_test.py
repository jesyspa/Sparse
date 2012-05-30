from nose.tools import eq_
from seval import seval
from SEnvironment import SEnvironment
from SNode import SNode
from stdenv import make_stdenv
import operator

def seval_num_test():
    eq_(seval('3'), 3)

def seval_add_test():
    eq_(seval('(+ 3 2)', make_stdenv()), 5)

def seval_mul_test():
    eq_(seval('(* 3 2)', make_stdenv()), 6)

def seval_eq_test():
    eq_(seval('(= 1 1)', make_stdenv()), True)

def seval_if_test():
    eq_(seval('(~if (= 1 1) 1 0)', make_stdenv()), 1)

def seval_env_test():
    env = SEnvironment()
    env.define('x', SNode('num', 5))
    eq_(seval('x', env), 5)

def seval_define_test():
    env = make_stdenv()
    seval('(~define x 5)', env)
    eq_(env.lookup('x'), SNode('num', 5))

def seval_lambda_test():
    eq_(seval('((~lambda () 5))', make_stdenv()), 5)

def seval_lambda_with_args_test():
    eq_(seval('((~lambda (x) x) 5)', make_stdenv()), 5)

def seval_quote_test():
    eq_(seval('(~quote (1 2 3))', make_stdenv()), (1, 2, 3))

def seval_quote_quote_test():
    eq_(seval('(~quote (~quote (1 2 3)))', make_stdenv()), ('~', 'quote', (1, 2, 3)))

def seval_cons_nil_test():
    eq_(seval('(cons 1 (cons 2 nil))', make_stdenv()), (1, 2))

def seval_head_test():
    eq_(seval("(head '(1 2 3))", make_stdenv()), 1)

def seval_tail_test():
    eq_(seval("(tail '(1 2 3))", make_stdenv()), (2, 3))
