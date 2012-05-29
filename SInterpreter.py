from sparse import sprint
from seval import seval
from SEnvironment import SEnvironment
import operator

class SInterpreter:
    """Provides a persistent environment for the evaluation of expressions."""
    def __init__(self):
        """Initialise the environment."""
        self._outer_scope = SEnvironment()
        self._outer_scope.define('+', lambda *args: sum(args))
        self._outer_scope.define('-', operator.sub)
        self._outer_scope.define('*', operator.mul)
        self._outer_scope.define('/', operator.floordiv)
        self._outer_scope.define('%', operator.mod)
        self._outer_scope.define('=', operator.eq)
        self._outer_scope.define('/=', operator.ne)
        self._outer_scope.define('<', operator.lt)
        self._outer_scope.define('>', operator.gt)
        self._outer_scope.define('<=', operator.le)
        self._outer_scope.define('>=', operator.ge)
        self._outer_scope.define('1-', lambda x: x+1)
        self._outer_scope.define('1+', lambda x: x-1)
        self._outer_scope.define('not', operator.not_)
        self._outer_scope.define('read-int', lambda: int(input('')))
        self._outer_scope.define('print', lambda x: sprint(x))
        self._outer_scope.define('apply', lambda f, args: f(*args))
        self._outer_scope.define('list', lambda *args: args)
        self._outer_scope.define('cons', lambda x, y: [x] + y)
        self._outer_scope.define('head', lambda x: x[0])
        self._outer_scope.define('tail', lambda x: x[1:])
        self._outer_scope.define('nil', tuple())
        self._outer_scope.define('#t', True)
        self._outer_scope.define('#f', False)

    def seval(self, string):
        """Parse the given code and return the result."""
        return seval(string, self._outer_scope)

