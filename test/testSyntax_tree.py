from unittest import TestCase

import homotopy.syntax_tree as st


class TestSyntaxTree(TestCase):
    def setUp(self):
        self.snippet = st.CompositeSnippet(st.SimpleSnippet('if'), '$', st.SimpleSnippet('i==1'))

    def test_repr(self):
        self.assertEqual(str(self.snippet), 'if$i==1')

    def test_eq(self):
        self.assertEqual(st.SimpleSnippet('if'),
                         st.SimpleSnippet('if'))

        self.assertEqual(st.CompositeSnippet(st.SimpleSnippet('if'), '$', st.SimpleSnippet('i==1')),
                         st.CompositeSnippet(st.SimpleSnippet('if'), '$', st.SimpleSnippet('i==1')))

        self.assertFalse(st.SimpleSnippet('if') != st.SimpleSnippet('if'))

    def test_compile(self):
        self.assertEqual(
            st.CompositeSnippet(
                st.CompositeSnippet(st.SimpleSnippet('for'), '#', st.SimpleSnippet('i')),
                '!',
                st.SimpleSnippet('data')
            ).compile(),
            'for i in data:\n\tpass'
        )
