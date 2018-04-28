from unittest import TestCase

from homotopy import homotopy


class TestStdlib(TestCase):
    def verifySingleSnippet(self, snippet, expected_output):
        homotopy_instance = homotopy.Homotopy(self.language)
        homotopy_instance.enable_cursor_marker()

        compiled_snippet = homotopy_instance.compile(snippet)

        self.assertEqual(expected_output.lstrip('\n').rstrip(), compiled_snippet)