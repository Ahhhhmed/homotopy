from unittest import TestCase
from unittest.mock import patch, MagicMock

import homotopy.syntax_tree as st
from homotopy.compiler import Compiler, ContextManager
from homotopy.snippet_provider import SnippetProvider


class TestCompiler(TestCase):
    def setUp(self):
        self.compiler_instance = Compiler(SnippetProvider())

    @patch('homotopy.snippet_provider.SnippetProvider.__getitem__')
    def test_compile(self, mock_provider):
        with self.assertRaises(NotImplementedError):
            self.compiler_instance.compile(st.Snippet())

        data = {
            "for": "for ### in !!!:\n\tpass",
            "def": "def !!!({{params}}):\n\tpass",
            "params": "###{{opt_params}}",
            "opt_params": ", ###{{opt_params}}",
            "multiple": "{{goo}}{{doo}}",
            "goo": "goo ###",
            "doo": "doo $$$",
            "outer": "param: ###, inside: >>>",
            "inner": "{{?###}} in: >>>"
        }

        mock_provider.side_effect = lambda x: x if x not in data else data[x]

        self.assertEqual(
            self.compiler_instance.compile(st.CompositeSnippet(
                st.CompositeSnippet(st.SimpleSnippet('for'), '#', st.SimpleSnippet('i')),
                '!',
                st.SimpleSnippet('data')
            )),
            'for i in data:\n\tpass'
        )

        self.assertEqual(
            self.compiler_instance.compile(st.CompositeSnippet(
                st.SimpleSnippet('multiple'),
                '$',
                st.SimpleSnippet('asd')
            )),
            'doo asd'
        )

        self.assertEqual(
            self.compiler_instance.compile(st.CompositeSnippet(
                st.SimpleSnippet('multiple'),
                '#',
                st.SimpleSnippet('asd')
            )),
            'goo asd'
        )

        with patch('logging.warning', MagicMock()) as m:
            self.assertEqual(
                self.compiler_instance.compile(st.CompositeSnippet(
                    st.CompositeSnippet(st.SimpleSnippet('for'), '#', st.SimpleSnippet('i')),
                    '%',
                    st.SimpleSnippet('data')
                )),
                'for i in !!!:\n\tpass'
            )

            m.assert_called_once_with("No match found. Ignoring right side of the snippet.")

        with patch('logging.warning', MagicMock()) as m:
            self.assertEqual(
                self.compiler_instance.compile(st.CompositeSnippet(
                    st.CompositeSnippet(
                        st.SimpleSnippet('doo'),
                        '$',
                        st.CompositeSnippet(
                            st.CompositeSnippet(
                                st.SimpleSnippet('def'),
                                '!',
                                st.SimpleSnippet('foo')
                            ),
                            '#',
                            st.SimpleSnippet('a')
                        )),
                    '#',
                    st.SimpleSnippet('b')
                )),
                'doo def foo(a):\n\tpass'
            )

            m.assert_called_once_with("No match found. Ignoring right side of the snippet.")

        self.assertEqual(
            self.compiler_instance.compile(st.CompositeSnippet(
                st.CompositeSnippet(st.SimpleSnippet('def'), '!', st.SimpleSnippet('foo')),
                '#',
                st.SimpleSnippet('a')
            )),
            'def foo(a):\n\tpass'
        )

        self.assertEqual(
            self.compiler_instance.compile(st.CompositeSnippet(
                st.CompositeSnippet(
                    st.CompositeSnippet(st.SimpleSnippet('def'), '!', st.SimpleSnippet('foo')),
                    '#',
                    st.SimpleSnippet('a')
                ),
                '#',
                st.SimpleSnippet('b'))),
            'def foo(a, b):\n\tpass'
        )

        self.assertEqual(
            self.compiler_instance.compile(st.CompositeSnippet(
                st.CompositeSnippet(
                    st.SimpleSnippet('outer'),
                    '#',
                    st.SimpleSnippet('test')
                ),
                '>',
                st.SimpleSnippet('inner'))),
            'param: test, inside: test in: >>>'
        )

        self.assertEqual(
            self.compiler_instance.compile(st.CompositeSnippet(
                st.CompositeSnippet(
                    st.SimpleSnippet('outer'),
                    '#',
                    st.SimpleSnippet('test')
                ),
                '>',
                st.CompositeSnippet(
                    st.SimpleSnippet('inner'),
                    '>',
                    st.SimpleSnippet('inner')
                ))),
            'param: test, inside: test in: test in: >>>'
        )


class TestContextManager(TestCase):
    def setUp(self):
        self.cm = ContextManager()

    def test_init(self):
        self.assertEqual([], self.cm.stack)

    def test_new_scope(self):
        self.cm.new_scope()

        self.assertEqual([{}], self.cm.stack)

    def test_remove_scope(self):
        self.cm.new_scope()
        self.cm.remove_scope()

        self.assertEqual([], self.cm.stack)

        self.cm.remove_scope()
        self.assertEqual([], self.cm.stack)

    def test_add_variable(self):
        with self.assertRaises(Exception) as context:
            self.cm.add_variable("x", "3")

        self.assertEqual("No scope to add variable to", str(context.exception))

        self.cm.new_scope()

        self.cm.add_variable("x", "3")
        self.assertEqual([{"x": "3"}], self.cm.stack)

        self.cm.add_variable("x", "4")
        self.assertEqual([{"x": "4"}], self.cm.stack)

        self.cm.add_variable("y", "3")
        self.assertEqual([{"x": "4", "y": "3"}], self.cm.stack)

    def test_get_item(self):
        self.assertEqual("", self.cm["x"])

        self.cm.new_scope()
        self.cm.add_variable("x", "3")
        self.cm.add_variable("y", "3")

        self.assertEqual("", self.cm["x"])

        self.cm.new_scope()
        self.assertEqual("3", self.cm["x"])

        self.cm.add_variable("x", "4")
        self.assertEqual("3", self.cm["x"])

        self.cm.remove_scope()
        self.assertEqual("", self.cm["x"])
