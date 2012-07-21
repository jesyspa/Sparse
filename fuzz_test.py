from sparse import sparse, sprint
from seval import seval_tree
from stdenv import make_stdenv
from SNode import SNode
from SException import SException
from random import random, randint, choice

def fuzz_test_generator():
    FUZZ_TIMES = 1
    program = sparse("""
    ((~lambda ()
      (~define x 10)
      (~define y 20)
      (~defun add (x y) (+ x y))
      (add (~if (< x y) x y) x)))
    """)
    for i in range(FUZZ_TIMES):
        env = make_stdenv()
        yield do_fuzz, random_modify(env, program), env

def make_list(env, tree, depth):
    def make_elements():
        for x in tree.value:
            r = random()
            if r < 0.8/depth:
                yield random_modify(env, x, depth+1)
            elif r < 0.85:
                yield x
            while random() < 0.1:
                yield random_modify(env, x, depth+1)
    return tuple(make_elements())

            

def random_modify(env, tree, depth=1):
    if random() < 0.05 and any(x.type == tree.type for x in env.values.values()):
        return SNode('id', choice([x for x in env.values if env.values[x].type ==
            tree.type]))
    if tree.type == 'list':
        return SNode('list', make_list(env, tree, depth))
    elif tree.type == 'id':
        return tree 
    elif tree.type == 'num':
        return SNode('num', randint(-1000000, 1000000))
    else:
        return tree

def record_issue(program, e):
    print("Issue found with:")
    sprint(program)
    print("Error: ", e)
    

def do_fuzz(program, env):
    try:
        sprint(program)
        seval_tree(program, env)
    except SException:
        pass

if __name__ == '__main__':
    fuzz_many()
