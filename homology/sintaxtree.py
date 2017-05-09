
class Snippet:
    pass

class CompositeSnippet(Snippet):
    """
    CompositeSnippet compose two snippets with the operand
    """
    def __init__(self, left, operation, right):
        self.left = left
        self.operation = operation
        self.right = right

    def __repr__(self):
        return str(self.left) + self.operation + str(self.right)

    def __eq__(self, other):
        return self.left == other.left and \
               self.operation == other.operation and\
               self.right == other.right


class SimpleSnippet(Snippet):
    """
    BasicSnippet can be directly compiled.
    """
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value