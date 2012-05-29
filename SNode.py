class SNode:
    def __init__(self, type, content):
        self.type = type
        self.content = content

    def __eq__(self, other):
        return self.type == other.type and self.content == other.content

    def __str__(self):
        if self.type == 'list':
            content = '({})'.format(', '.join([str(n) for n in self.content]))
        else:
            content = self.content
        return "({}, {})".format(repr(self.type), content)

    def __hash__(self):
        return hash(self.type) ^ hash(self.content)
