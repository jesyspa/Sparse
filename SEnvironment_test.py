from nose.tools import eq_, raises
from SEnvironment import SEnvironment

def SEnv_define_test():
    e = SEnvironment()
    e.define('x', 5)

def SEnv_lookup_test():
    e = SEnvironment()
    e.define('x', 5)
    eq_(e.lookup('x'), 5)

def SEnv_set_test():
    e = SEnvironment()
    e.define('x', 3)
    e.set('x', 5)
    eq_(e.lookup('x'), 5)

def SEnv_parent_lookup_test():
    p = SEnvironment()
    p.define('x', 5)
    e = SEnvironment(p)
    eq_(e.lookup('x'), 5)

def SEnv_parent_set_test():
    p = SEnvironment()
    p.define('x', 3)
    e = SEnvironment(p)
    e.set('x', 5)
    eq_(e.lookup('x'), 5)
    eq_(p.lookup('x'), 5)

def SEnv_parent_redefine_test():
    p = SEnvironment()
    p.define('x', 3)
    e = SEnvironment(p)
    e.define('x', 5)
    eq_(e.lookup('x'), 5)
    eq_(p.lookup('x'), 3)

@raises(Exception)
def SEnv_use_undefined_variable_test():
    p = SEnvironment()
    p.lookup('x')

@raises(Exception)
def SEnv_set_undefined_variable_test():
    p = SEnvironment()
    p.set('x', 3)

def SEnv_contains_test():
    p = SEnvironment()
    assert not 'x' in p
    p.define('x', 3)
    assert 'x' in p
