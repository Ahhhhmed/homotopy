from homotopy.syntax_tree import SnippetVisitor
from homotopy.parser import Parser

import re
import logging


class Compiler(SnippetVisitor):
    """
    Compiler for snippets. Turns syntax tree into text.
    """
    def __init__(self, snippet_provider):
        self.context_manager = ContextManager()
        self.context_manager.new_scope()
        self.snippet_provider = snippet_provider

    def visit_composite_snippet(self, composite_snippet):
        """
        Replace right site in the appropriate place in the left side.
        Expand left side if needed. Manage scopes.

        :param composite_snippet: Composite snippet
        :return: Text of left side replaced with right side
        """
        left_side = self.expand_variable_operators(self.snippet_provider[self.visit(composite_snippet.left)])

        if composite_snippet.operation == Parser.in_operator:
            self.context_manager.new_scope()

        right_side = self.snippet_provider[self.compile(composite_snippet.right)]

        if composite_snippet.operation == Parser.in_operator:
            self.context_manager.remove_scope()

        operation_text = composite_snippet.operation*3

        if operation_text in left_side:
            return self.substitute(left_side, operation_text, right_side)
        else:
            expanded_left_side = left_side
            match_found = False

            def expansion_function(match_object):
                nonlocal match_found

                if not match_found and operation_text in self.snippet_provider[match_object.group(1)]:
                    match_found = True
                    return self.snippet_provider[match_object.group(1)]

                return match_object.group(0)

            expanded_left_side = re.sub(
                r'{{(.*?)}}',
                expansion_function,
                expanded_left_side)

            if operation_text in expanded_left_side:
                return self.substitute(expanded_left_side, operation_text, right_side)

        logging.warning("No match found. Ignoring right side of the snippet.")
        return left_side

    def visit_simple_snippet(self, simple_snippet):
        """
        Compile simple snippet.

        :param simple_snippet: Simple snippet
        :return: Text of compile snippet
        """
        return self.expand_variable_operators(self.snippet_provider[simple_snippet.value])

    def expand_variable_operators(self, text):
        """
        Expend parameter variables.

        :param text: Text
        :return: Expended text
        """
        return re.sub(
            r'{{[?](.*?)}}',
            lambda match_group: self.context_manager[match_group.group(1)],
            text)

    def substitute(self, left, operation, right):
        if operation != Parser.in_operator:
            self.context_manager.add_variable(operation, right)
        return left.replace(operation, right)

    def compile(self, snippet):
        """
        Compile a snippet. Visit and then perform a clean.

        :param snippet: Snippet
        :return: Text of compiled snippet
        """
        compiled_snippet = self.visit(snippet)

        return re.sub(r'({{.*?}})', "", compiled_snippet)


class ContextManager:
    """
    Class for managing substituted parameters to be used again.
    """
    def __init__(self):
        """
        Initialize stack.
        """
        self.stack = []

    def new_scope(self):
        """
        Add new scope.
        """
        self.stack.append({})

    def remove_scope(self):
        """
        Remove last scope.
        """
        if self.stack:
            self.stack.pop()

    def add_variable(self, name, value):
        """
        Add variable to current scope.

        :param name: Variable name
        :param value: Variable value
        """
        if self.stack:
            self.stack[-1][name] = value
        else:
            raise Exception("No scope to add variable to")

    def __getitem__(self, item):
        """
        Get variable from last scope.

        :param item: Variable name
        :return: Variable value if it exists. Empty string otherwise
        """
        if len(self.stack) < 2 or item not in self.stack[-2]:
            return ""

        return self.stack[-2][item]
