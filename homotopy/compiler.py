from homotopy.syntax_tree import SnippetVisitor
from homotopy.snippet_provider import snippetProvider

import re
import logging


class Compiler(SnippetVisitor):
    def visit_composite_snippet(self, composite_snippet):
        left_side = snippetProvider[self.visit(composite_snippet.left)]
        right_side = snippetProvider[self.compile(composite_snippet.right)]

        operation_text = composite_snippet.operation*3

        if operation_text in left_side:
            return left_side.replace(operation_text, right_side)
        else:
            expanded_left_side = left_side
            match_found = False

            def expansion_function(match_object):
                nonlocal match_found

                if not match_found and operation_text in snippetProvider[match_object.group(1)]:
                    match_found = True
                    return snippetProvider[match_object.group(1)]

                return match_object.group(0)

            expanded_left_side = re.sub(
                r'{{(.*?)}}',
                expansion_function,
                expanded_left_side)

            if operation_text in expanded_left_side:
                return expanded_left_side.replace(operation_text, right_side)

        logging.warning("No match found. Ignoring right side of the snippet.")
        return left_side

    def visit_simple_snippet(self, simple_snippet):
        return snippetProvider[simple_snippet.value]

    def compile(self, snippet):
        compiled_snippet = self.visit(snippet)

        return re.sub(r'({{.*?}})', "", compiled_snippet)

