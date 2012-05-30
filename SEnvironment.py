class SEnvironment:
    """Represents a layered symbol table."""
    def __init__(self, parent=None):
        """Initialise with the given parent and no symbols."""
        self._parent = parent
        self.values = {}

    @property
    def parent(self):
        assert self._parent is not None, (
                "Parent environment of global requested.")
        return self._parent

    def lookup(self, key):
        """Return the value associated with the given key.
        
        Raises Exception if no such key exists.

        """
        env = self._get_env_with(key)
        if env is None:
            raise Exception("Use of undefined variable {}.".format(key))
        return env[key]

    def set(self, key, value):
        """Set the value associated with the given key.

        Raises Exception if no such key exists.

        """
        env = self._get_env_with(key)
        if env is None:
            raise Exception("Cannot set undefined variable {}.".format(key))
        env[key] = value

    def define(self, key, value):
        """Create a value associated with the given key in this layer."""
        self.values[key] = value

    def _get_env_with(self, key):
        """Returns the topmost dictionary that contains key, or None."""
        if key in self.values:
            return self.values
        if self._parent is not None:
            return self._parent._get_env_with(key)
        return None

    def __contains__(self, item):
        """Check whether any of the layers contains the given key."""
        return self._get_env_with(item) is not None

