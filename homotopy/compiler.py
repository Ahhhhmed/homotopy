from homotopy.syntax_tree import SnippetVisitor
from homotopy.snippet_provider import snippetProvider

import re
import logging


class Compiler(SnippetVisitor):
    def __init__(self, expansion_level_count=2):
        self.expansion_level_count = expansion_level_count

    def visit_composite_snippet(self, composite_snippet):
        left_side = snippetProvider[self.visit(composite_snippet.left)]
        right_side = snippetProvider[self.visit(composite_snippet.right)]

        if composite_snippet.operation in left_side:
            return left_side.replace(composite_snippet.operation, right_side)
        else:
            expanded_left_side = left_side

            for _ in range(self.expansion_level_count):
                expanded_left_side = re.sub(
                    r'{{(.*?)}}',
                    lambda match_object: snippetProvider[match_object.group(1)],
                    expanded_left_side,
                    count=1)

                if composite_snippet.operation in expanded_left_side:
                    return expanded_left_side.replace(composite_snippet.operation, right_side)

        logging.warning("No match found. Ignoring right side of the snippet.")
        return left_side

    def visit_simple_snippet(self, simple_snippet):
        return snippetProvider[simple_snippet.value]

    def compile(self, snippet):
        compiled_snippet = self.visit(snippet)

        return re.sub(r'({{.*?}})', "", compiled_snippet)

