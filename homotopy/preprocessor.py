from homotopy.snippet_provider import snippetProvider

import re


class Preprocessor:
    cursor_marker = "[{cursor_marker}]"

    @staticmethod
    def expand_decorators(snippet_text):
        return re.sub(
                r'\[\[(.*?)\]\]',
                lambda match_group: snippetProvider[match_group.group(1)],
                snippet_text)

    @staticmethod
    def put_cursor_marker(snippet_text):
        return snippet_text + "&" + Preprocessor.cursor_marker
