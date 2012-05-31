from nose.tools import eq_
from SNode import SNode
from sparse import sparse, sunparse
from seval import seval, seval_strip
from stdenv import make_stdenv

def stdenv_if_test():
    eq_(seval_strip('(~if (= 1 1) 1 0)', make_stdenv()), 1)

def stdenv_define_test():
    env = make_stdenv()
    seval_strip('(~define x 5)', env)
    eq_(env.lookup('x'), SNode('num', 5))

def stdenv_lambda_test():
    eq_(seval_strip('((~lambda () 5))', make_stdenv()), 5)

def stdenv_lambda_with_args_test():
    eq_(seval_strip('((~lambda (x) x) 5)', make_stdenv()), 5)

def stdenv_quote_test():
    eq_(seval_strip('(~quote (1 2 3))', make_stdenv()), (1, 2, 3))

def stdenv_quote_quote_test():
    eq_(seval_strip('(~quote (~quote (1 2 3)))', make_stdenv()), ('~', 'quote', (1, 2, 3)))

def stdenv_cons_nil_test():
    eq_(seval_strip('(cons 1 (cons 2 nil))', make_stdenv()), (1, 2))

def stdenv_head_test():
    eq_(seval_strip("(head '(1 2 3))", make_stdenv()), 1)

def stdenv_tail_test():
    eq_(seval_strip("(tail '(1 2 3))", make_stdenv()), (2, 3))

def stdenv_quasiquote_test():
    eq_(seval_strip('`(1 2)', make_stdenv()), (1, 2))

def stdenv_unquote_test():
    eq_(seval_strip('`(1 ,(+ 1 1))', make_stdenv()), (1, 2))

def stdenv_eval_test():
    eq_(seval_strip('(eval `(+ 1 1) (this-env))', make_stdenv()), 2)

def stdenv_restargs_test():
    eq_(seval_strip('((~lambda (x . y) (apply + y)) 1 2 3)', make_stdenv()), 5)

def stdenv_apply_test():
    eq_(seval_strip('(apply + `(2 3))', make_stdenv()), 5)

def stdenv_defun_test():
    env = make_stdenv()
    seval('(~defun add (a b) (+ a b))', env)
    eq_(seval_strip('(add 1 2)', env), 3)

def stdenv_append_test():
    eq_(seval_strip('(~append (1 2) (3 4) (5))', make_stdenv()), (1, 2, 3, 4, 5))

def seval_unquote_splice_test():
    eq_(seval_strip("`(1 ,@'(2))", make_stdenv()), (1, 2))
