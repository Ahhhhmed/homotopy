from unittest import TestCase
from unittest.mock import patch

from homotopy.preprocessor import Preprocessor
from homotopy.snippet_provider import SnippetProvider


class TestPreprocessor(TestCase):
    def setUp(self):
        self.preprocessor_instance = Preprocessor(SnippetProvider("", []))

    @patch('homotopy.snippet_provider.SnippetProvider.__getitem__')
    def test_expand_decorators(self, mock_provider):
        data = {
            "def": "expansion",
            "def1": "expansion1",
            "def2": "expansion2"
        }

        mock_provider.side_effect = lambda x: x if x not in data else data[x]

        self.assertEqual("noExpansion", self.preprocessor_instance.expand_decorators("noExpansion"))

        self.assertEqual("test_expansion", self.preprocessor_instance.expand_decorators("test_[[def]]"))

        self.assertEqual("multiple_expansion1_expansions_expansion2",
                         self.preprocessor_instance.expand_decorators("multiple_[[def1]]_expansions_[[def2]]"))

    def test_put_cursor_marker(self):
        cursor_marker = "[{cursor_marker}]"

        self.assertEqual("snippet&" + cursor_marker, self.preprocessor_instance.put_cursor_marker("snippet"))
