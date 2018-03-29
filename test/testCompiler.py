from unittest import TestCase
from unittest.mock import patch, MagicMock

import homotopy.syntax_tree as st
from homotopy.compiler import Compiler


class TestCompiler(TestCase):
    @patch('homotopy.snippet_provider.SnippetProvider.__getitem__')
    def test_compile(self, mock_provider):
        with self.assertRaises(NotImplementedError):
            Compiler().compile(st.Snippet())

        data = {
            "for": "for # in !:\n\tpass",
            "def": "def !({{params}}):\n\tpass",
            "params": "#{{opt_params}}",
            "opt_params": ", #{{opt_params}}",
            "a1": "{{a2}}",
            "a2": "{{a3}}",
            "a3": "{{a4}}",
            "a4": "#"
        }

        mock_provider.side_effect = lambda x: x if x not in data else data[x]

        self.assertEqual(
            Compiler().compile(st.CompositeSnippet(
                st.CompositeSnippet(st.SimpleSnippet('for'), '#', st.SimpleSnippet('i')),
                '!',
                st.SimpleSnippet('data')
            )),
            'for i in data:\n\tpass'
        )

        with patch('logging.warning', MagicMock()) as m:
            self.assertEqual(
                Compiler().compile(st.CompositeSnippet(
                    st.CompositeSnippet(st.SimpleSnippet('for'), '#', st.SimpleSnippet('i')),
                    '%',
                    st.SimpleSnippet('data')
                )),
                'for i in !:\n\tpass'
            )

            m.assert_called_once_with("No match found. Ignoring right side of the snippet.")

        with patch('logging.warning', MagicMock()) as m:
            self.assertEqual(
                Compiler().compile(st.CompositeSnippet(st.SimpleSnippet('a1'), '#', st.SimpleSnippet('i'))),
                ''
            )

            self.assertEqual(
                Compiler(expansion_level_count=3).compile(st.CompositeSnippet(st.SimpleSnippet('a1'), '#', st.SimpleSnippet('i'))),
                'i'
            )

            m.assert_called_once_with("No match found. Ignoring right side of the snippet.")

        self.assertEqual(
            Compiler().compile(st.CompositeSnippet(
                st.CompositeSnippet(st.SimpleSnippet('def'), '!', st.SimpleSnippet('foo')),
                '#',
                st.SimpleSnippet('a')
            )),
            'def foo(a):\n\tpass'
        )

        self.assertEqual(
            Compiler().compile(st.CompositeSnippet(
                st.CompositeSnippet(
                    st.CompositeSnippet(st.SimpleSnippet('def'), '!', st.SimpleSnippet('foo')),
                    '#',
                    st.SimpleSnippet('a')
                ),
                '#',
                st.SimpleSnippet('b'))),
            'def foo(a, b):\n\tpass'
        )
