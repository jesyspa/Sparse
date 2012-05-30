from nose.tools import eq_
from SNode import SNode
from sparse import sparse, sunparse
from seval import seval, seval_strip
from stdenv import make_stdenv

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
