from unittest import TestCase
from unittest.mock import patch

import homotopy.syntax_tree as st


class TestSyntaxTree(TestCase):
    def test_repr(self):
        self.snippet = st.CompositeSnippet(st.SimpleSnippet('if'), '$', st.SimpleSnippet('i==1'))
        self.assertEqual(str(self.snippet), 'if$i==1')

    def test_eq(self):
        # should not be equal to any instance of any other type
        self.assertTrue(st.SimpleSnippet('if') != 123)
        self.assertTrue(st.CompositeSnippet(None, None, None) != 123)

        self.assertEqual(st.SimpleSnippet('if'),
                         st.SimpleSnippet('if'))

        self.assertEqual(st.CompositeSnippet(st.SimpleSnippet('if'), '$', st.SimpleSnippet('i==1')),
                         st.CompositeSnippet(st.SimpleSnippet('if'), '$', st.SimpleSnippet('i==1')))

        self.assertFalse(st.SimpleSnippet('if') != st.SimpleSnippet('if'))

    @patch('homotopy.snippet_provider.SnippetProvider.__getitem__')
    def test_compile(self, mockProvider):
        self.assertIsNone(st.Snippet().compile())

        mockProvider.side_effect = lambda x: x if x != "for" else "for # in !:\n\tpass"

        self.assertEqual(
            st.CompositeSnippet(
                st.CompositeSnippet(st.SimpleSnippet('for'), '#', st.SimpleSnippet('i')),
                '!',
                st.SimpleSnippet('data')
            ).compile(),
            'for i in data:\n\tpass'
        )
