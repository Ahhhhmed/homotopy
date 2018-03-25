from homotopy.snippet_provider import snippetProvider


class Snippet:
    def compile(self):
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
        if isinstance(other, self.__class__):
            return self.left == other.left and \
                   self.operation == other.operation and\
                   self.right == other.right
        return False

    def compile(self):
        return snippetProvider[self.left.compile()].replace(self.operation, snippetProvider[self.right.compile()])



class SimpleSnippet(Snippet):
    """
    BasicSnippet can be directly compiled.
    """
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        return False

    def compile(self):
        return snippetProvider[self.value]
