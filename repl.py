#!/usr/bin/python

from sparse import sprint
from SInterpreter import SInterpreter
from SException import SException

def main():
    """Run the REPL."""
    interp = SInterpreter()
    while True:
        try:
            line = input('>>> ')
            while line.count('(') > line.count(')'):
                line += ' ' + input('... ' + ' ' * 2 * (line.count('(') -
                    line.count(')')))
            if line.count('(') < line.count(')'):
                raise Exception("Too many closing parentheses.")
            sprint(interp.seval(line))
        except EOFError:
            print('Bye')
            return
        except SException as e:
            print('Error:', e)
    

if __name__ == '__main__':
    main()
