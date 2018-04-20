

class Snippet:
    """
    Base class for snippet syntax tree.
    """
    def accept(self, visitor):
        """
        Accepts a visitor

        :param visitor: Visitor instance
        :return: Visitor result
        """
        raise NotImplementedError("You should not be here.")


class CompositeSnippet(Snippet):
    """
    CompositeSnippet compose two snippets with the operand
    """
    def __init__(self, left, operation, right):
        """
        Initialize CompositeSnippet instance.

        :param left: Left subtree
        :param operation: Operation
        :param right: Right subtree
        """
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

    def accept(self, visitor):
        return visitor.visit_composite_snippet(self)


class SimpleSnippet(Snippet):
    """
    BasicSnippet can be directly compiled.
    """
    def __init__(self, value):
        """
        Initialize SimpleSnippet instance.

        :param value: Value of the snippet
        """
        self.value = value

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        return False

    def accept(self, visitor):
        return visitor.visit_simple_snippet(self)


class SnippetVisitor:
    """
    Base class for visitors working on syntax tree.
    """
    def visit(self, snippet):
        return snippet.accept(self)

    def visit_composite_snippet(self, composite_snippet):
        """
        Base visit logic for composite snippets. Process right and left subtrees recursively.

        :param composite_snippet: CompositeSnippet instance
        :return: None
        """
        composite_snippet.left.accept(self)
        composite_snippet.right.accept(self)

    def visit_simple_snippet(self, simple_snippet):
        """
        Base visit logic for simple snippets. Does nothing.

        :param simple_snippet: SimpleSnippet instance
        :return: None
        """
        pass
