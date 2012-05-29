class SNode:
    """Represent a single element of the grammar."""
    def __init__(self, type, value):
        """Initialise given the type and value."""
        self.type = type
        self.value = value

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __str__(self):
        if self.type == 'list':
            value = '({})'.format(', '.join([str(n) for n in self.value]))
        else:
            value = self.value
        return "({}, {})".format(repr(self.type), value)

    def __hash__(self):
        return hash(self.type) ^ hash(self.value)
