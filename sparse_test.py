from nose.tools import eq_
from sparse import sparse, sunparse
from SNode import SNode

def sparse_num_test():
    eq_(sparse('5'), SNode('num', 5))

def sparse_id_test():
    eq_(sparse('x'), SNode('id', 'x'))

def sparse_empty_list_test():
    eq_(sparse('()'), SNode('list', tuple()))

def sparse_two_element_list_test():
    eq_(sparse('(x y)'), SNode('list', (SNode('id', 'x'), SNode('id', 'y'))))

def sparse_nested_list_test():
    eq_(sparse('(a (b c) d)'), SNode('list', (SNode('id', 'a'), SNode('list',
        (SNode('id', 'b'), SNode('id', 'c'))), SNode('id', 'd'))))

def sparse_sunparse_num_test():
    eq_(sunparse(sparse('5')), '5')

def sparse_sunparse_id_test():
    eq_(sunparse(sparse('a')), 'a')

def sparse_sunparse_list_test():
    eq_(sunparse(sparse('(1 b)')), '(1 b)')

def sparse_quote_num_test():
    eq_(sunparse(sparse("'5")), '(~ quote 5)')

def sparse_quote_id_test():
    eq_(sunparse(sparse("'x")), '(~ quote x)')

def sparse_quote_list_test():
    eq_(sunparse(sparse("'(1 2)")), '(~ quote (1 2))')

def sparse_sf_test():
    eq_(sparse("(~)"), SNode('list', (SNode('sf', '~'),)))

def sparse_quasiquote_test():
    eq_(sunparse(sparse("`(a b)")), '(~ quasiquote (a b))')

def sparse_unquote_test():
    eq_(sunparse(sparse("`(a ,b)")), '(~ quasiquote (a (unquote b)))')

def sparse_dot_test():
    eq_(sunparse(sparse("(1 . 2)")), '((1) 2)')

