from nose.tools import eq_
from SInterpreter import SInterpreter

def SInterp_basic_eval_test():
    interp = SInterpreter()
    eq_(interp.seval('(+ 3 2)'), 5)

def SInterp_define_test():
    interp = SInterpreter()
    interp.seval('(define x 5)')
    eq_(interp.seval('x'), 5)

def SInterp_recursive_test():
    interp = SInterpreter()
    interp.seval('(define f (lambda (y) (if (= y 0) 0 (f (- y 1)))))')
    eq_(interp.seval('(f 2)'), 0)
