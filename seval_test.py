from nose.tools import eq_
from seval import seval_strip
from SEnvironment import SEnvironment
from SNode import SNode
from stdenv import make_stdenv
import operator

def seval_num_test():
    eq_(seval_strip('3'), 3)

def seval_funcall_test():
    eq_(seval_strip('(+ 3 2)', make_stdenv()), 5)

def seval_env_test():
    env = SEnvironment()
    env.define('x', SNode('num', 5))
    eq_(seval_strip('x', env), 5)

