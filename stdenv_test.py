from nose.tools import eq_
from SNode import SNode
from sparse import sparse, sunparse
from seval import seval, seval_strip
from stdenv import make_stdenv

def stdenv_quasiquote_test():
    eq_(seval_strip('`(1 2)', make_stdenv()), (1, 2))

def stdenv_unquote_test():
    eq_(seval_strip('`(1 ,(+ 1 1))', make_stdenv()), (1, 2))
