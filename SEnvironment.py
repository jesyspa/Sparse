class SEnvironment:
    def __init__(self, parent=None):
        self.parent = parent
        self.values = {}

    def lookup(self, key):
        env = self._get_env_with(key)
        if env is None:
            raise Exception("Use of undefined variable {}.".format(key))
        return env[key]

    def set(self, key, value):
        env = self._get_env_with(key)
        if env is None:
            raise Exception("Cannot set undefined variable {}.".format(key))
        env[key] = value

    def define(self, key, value):
        self.values[key] = value

    def _get_env_with(self, key):
        if key in self.values:
            return self.values
        if self.parent is not None:
            return self.parent._get_env_with(key)
        return None
