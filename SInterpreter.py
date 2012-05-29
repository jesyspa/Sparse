from sparse import sprint
from seval import seval
from SEnvironment import SEnvironment
from stdenv import make_stdenv
import operator

class SInterpreter:
    """Provides a persistent environment for the evaluation of expressions."""
    def __init__(self):
        """Initialise the environment."""
        self._env, self._menv = make_stdenv()

    def seval(self, string):
        """Parse the given code and return the result."""
        return seval(string, self._env, self._menv)

