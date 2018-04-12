import os
import json
import logging


class SnippetProvider:
    """
    Class for translating simple snippets into code.
    Uses a database provided in json files located in the path variable.
    """

    def __init__(self, language="", path=[]):
        """
        Initialize snippet provider instance.

        :param language: language to compile to
        :param path: list of directories to search for json files containing snippets
        """
        self.data = {}
        self.language = language
        self.path = path
        for item in self.path:
            for file in filter(lambda x: x.endswith(".json"), os.listdir(item)):
                try:
                    for snippet in filter(lambda x: x["language"].lower() == self.language.lower(), json.load(open(os.path.join(item, file)))):
                        if snippet["name"] in self.data:
                            logging.warning("Multiple definition for %s" % snippet["name"])
                        else:
                            self.data[snippet["name"]] = snippet["snippet"]
                except (ValueError, OSError):
                    logging.warning("Could not get data from file %s" % file, exc_info=True)

    def __getitem__(self, item):
        """
        Expand single snippet.

        :param item: snippet
        :return: snippet expansion
        """
        if item in self.data:
            return self.data[item]
        return item


stdlib_path = os.path.join(os.path.split(__file__)[0], 'stdlib')

snippetProvider = SnippetProvider(language='c++', path=[stdlib_path])
