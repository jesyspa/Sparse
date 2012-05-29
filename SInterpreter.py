from seval import seval
from SEnvironment import SEnvironment
import operator

class SInterpreter:
    def __init__(self):
        self._outer_scope = SEnvironment()
        self._outer_scope.define('+', lambda *args: sum(args))
        self._outer_scope.define('-', operator.sub)
        self._outer_scope.define('*', operator.mul)
        self._outer_scope.define('/', operator.floordiv)
        self._outer_scope.define('%', operator.mod)
        self._outer_scope.define('=', operator.eq)
        self._outer_scope.define('<', operator.lt)
        self._outer_scope.define('>', operator.gt)
        self._outer_scope.define('<=', operator.le)
        self._outer_scope.define('>=', operator.ge)
        self._outer_scope.define('read-int', lambda: int(input('')))
        self._outer_scope.define('print', lambda x: print(x))

    def seval(self, string):
        return seval(string, self._outer_scope)

