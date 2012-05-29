#!/usr/bin/python

from SInterpreter import SInterpreter

def main():
    interp = SInterpreter()
    try:
        while True:
            print(interp.seval(input('>>> ')))
    except EOFError:
        print('Bye')

if __name__ == '__main__':
    main()
