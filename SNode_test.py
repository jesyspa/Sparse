from nose.tools import eq_
from SNode import SNode

def SNode_type_test():
    n = SNode('id', 'x')
    eq_(n.type, 'id')

def SNode_value_test():
    n = SNode('id', 'x')
    eq_(n.value, 'x')

def SNode_eq_test():
    eq_(SNode('id', 'x'), SNode('id', 'x'))
