from homotopy.snippet_provider import snippetProvider

import re


class Preprocessor:
    """
    Prepossess snippet text to enable extra feathers.
    """
    cursor_marker = "[{cursor_marker}]"

    @staticmethod
    def expand_decorators(snippet_text):
        """
        Expand decorators to enable concise writing of common patterns.

        :param snippet_text: Snippet text
        :return: Expanded snippet text
        """
        return re.sub(
                r'\[\[(.*?)\]\]',
                lambda match_group: snippetProvider[match_group.group(1)],
                snippet_text)

    @staticmethod
    def put_cursor_marker(snippet_text):
        """
        Put cursor marker witch should be used by editor plugins for better experience.

        :param snippet_text: Snippet text
        :return: Snippet text with marker at the end
        """
        return snippet_text + "&" + Preprocessor.cursor_marker
