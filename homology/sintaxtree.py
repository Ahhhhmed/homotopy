
class Snippet:
    pass

class CompositeSnippet(Snippet):
    """
    CompositeSnippet compose two snippets with the operand
    """
    def __init__(self, left, operand, right):
        self.left = left
        self.operand = operand
        self.right = right

    def __repr__(self):
        return str(self.left) + self.operand + str(self.right)


class BasicSnippet(Snippet):
    """
    BasicSnippet can be directly compiled.
    """
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value