import re


class Preprocessor:
    """
    Prepossess snippet text to enable extra feathers.
    """
    cursor_marker = "[{cursor_marker}]"

    def __init__(self, snippet_provider):
        """
        Initialize preprocessor instance.

        :param snippet_provider: Snippet provider
        """
        self.snippet_provider = snippet_provider

    def expand_decorators(self, snippet_text):
        """
        Expand decorators to enable concise writing of common patterns.

        :param snippet_text: Snippet text
        :return: Expanded snippet text
        """
        return re.sub(
                r'\[\[(.*?)\]\]',
                lambda match_group: self.snippet_provider[match_group.group(1)],
                snippet_text)

    @staticmethod
    def put_cursor_marker(snippet_text):
        """
        Put cursor marker witch should be used by editor plugins for better experience.

        :param snippet_text: Snippet text
        :return: Snippet text with marker at the end
        """
        return snippet_text + "&" + Preprocessor.cursor_marker
