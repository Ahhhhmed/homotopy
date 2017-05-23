

class SnippetProvider:
    """
    Class for translating simple snippets into code.
    """

    data = {
        "for": "for # in %:\n\tpass"
    }

    def __getitem__(self, item):
        if item in SnippetProvider.data:
            return SnippetProvider.data[item]
        return item
