import os
import json
import logging


class SnippetProvider:
    """
    Class for translating simple snippets into code.
    Uses a database provided in json files located in the path variable.
    """

    language_key = "language"
    name_key = "name"
    snippet_key = "snippet"

    def __init__(self, language, path):
        """
        Initialize snippet provider instance.

        :param language: language to compile to
        :param path: list of directories to search for json files containing snippets
        """
        self.data = {}
        self.language = language
        self.path = path
        for item in self.path:
            for file_name in filter(lambda x: x.endswith(".json"), os.listdir(item)):
                try:
                    def language_filter(filter_item):
                        all_languages = 'all'

                        languages = [filter_item[SnippetProvider.language_key].lower()] \
                            if type(filter_item[SnippetProvider.language_key]) is str \
                            else [x.lower() for x in filter_item[SnippetProvider.language_key]]

                        if '~' + self.language.lower() in languages:
                            return False

                        return all_languages in languages or self.language.lower() in languages

                    with open(os.path.join(item, file_name)) as opened_file:
                        for snippet in filter(language_filter, json.load(opened_file)):
                            if snippet[SnippetProvider.name_key] in self.data:
                                logging.warning("Multiple definition for %s" % snippet[SnippetProvider.name_key])
                            else:
                                self.data[snippet[SnippetProvider.name_key]] = snippet[SnippetProvider.snippet_key]
                except (ValueError, OSError):
                    logging.warning("Could not get data from file %s" % file_name, exc_info=True)

    def __getitem__(self, item):
        """
        Expand single snippet.

        :param item: snippet
        :return: snippet expansion
        """
        if item in self.data:
            return self.data[item]
        return item
