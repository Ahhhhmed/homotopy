from unittest import TestCase
from unittest.mock import patch, call

import homotopy.syntax_tree as st
from homotopy.code_generator import CodeGenerator, ContextManager
from homotopy.snippet_provider import SnippetProvider
from homotopy.util import IndentManager


class TestCodeGenerator(TestCase):
    def setUp(self):
        self.code_generator_instance = CodeGenerator(SnippetProvider("", []), IndentManager())

    @patch('homotopy.util.IndentManager.indent_new_lines')
    @patch('homotopy.snippet_provider.SnippetProvider.__getitem__')
    def test_compile(self, mock_provider, mock_indent_new_lines):
        with self.assertRaises(NotImplementedError):
            self.code_generator_instance.generate_code(st.Snippet())

        data = {
            "for": "for ### in !!!:\n\tpass",
            "def": "def !!!({{params}}):\n\tpass",
            "params": "###{{opt_params}}",
            "opt_params": ", ###{{opt_params}}",
            "multiple": "{{goo}}{{doo}}",
            "regextest": "{{{goo}}{{{doo}}}",
            "goo": "goo ###",
            "doo": "doo $$$",
            "outer": "param: ###, inside: >>>",
            "inner": "{{?###}} in: >>>"
        }

        mock_provider.side_effect = lambda x: x if x not in data else data[x]
        mock_indent_new_lines.side_effect = lambda x, _: x

        self.assertEqual(
            self.code_generator_instance.generate_code(st.CompositeSnippet(
                st.CompositeSnippet(st.SimpleSnippet('for'), '#', st.SimpleSnippet('i')),
                '!',
                st.SimpleSnippet('data')
            )),
            'for i in data:\n\tpass'
        )

        self.assertEqual(
            self.code_generator_instance.generate_code(st.CompositeSnippet(
                st.SimpleSnippet('multiple'),
                '$',
                st.SimpleSnippet('asd')
            )),
            'doo asd'
        )

        self.assertEqual(
            self.code_generator_instance.generate_code(st.CompositeSnippet(
                st.SimpleSnippet('regextest'),
                '#',
                st.SimpleSnippet('asd')
            )),
            '{goo asd{}'
        )

        self.assertEqual(
            self.code_generator_instance.generate_code(st.CompositeSnippet(
                st.SimpleSnippet('multiple'),
                '#',
                st.SimpleSnippet('asd')
            )),
            'goo asd'
        )

        with patch('homotopy.code_generator.ContextManager.add_variable') as mock_add_variable:
            self.assertEqual(
                self.code_generator_instance.generate_code(st.CompositeSnippet(
                    st.CompositeSnippet(st.SimpleSnippet('for'), '#', st.SimpleSnippet('i')),
                    '%',
                    st.SimpleSnippet('data')
                )),
                'for i in !!!:\n\tpass'
            )

            mock_add_variable.assert_has_calls([
                call('###', 'i'),
                call('%%%', 'data')
            ])

        self.assertEqual(
            self.code_generator_instance.generate_code(st.CompositeSnippet(
                st.CompositeSnippet(st.SimpleSnippet('def'), '!', st.SimpleSnippet('foo')),
                '#',
                st.SimpleSnippet('a')
            )),
            'def foo(a):\n\tpass'
        )

        self.assertEqual(
            self.code_generator_instance.generate_code(st.CompositeSnippet(
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
            self.code_generator_instance.generate_code(st.CompositeSnippet(
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
            self.code_generator_instance.generate_code(st.CompositeSnippet(
                st.SimpleSnippet("goo"),
                '#',
                st.SimpleSnippet('goo'))),
            'goo goo'
        )

        self.assertEqual(
            self.code_generator_instance.generate_code(st.CompositeSnippet(
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

    @patch('homotopy.util.IndentManager.indent_new_lines')
    @patch('homotopy.snippet_provider.SnippetProvider.__getitem__')
    def test_indentation(self, mock_provider, mock_indent_new_lines):
        with self.assertRaises(NotImplementedError):
            self.code_generator_instance.generate_code(st.Snippet())

        data = {
            "for": "for item in collection:\n\t  \t {{helper}}",
            "helper": ">>>",
            "if": "if(true){\n{{inside_block}}\n}",
            "inside_block": "\t>>>{{opt_inside_block}}",
            "opt_inside_block": "\n\t>>>{{opt_inside_block}}"
        }

        mock_provider.side_effect = lambda x: x if x not in data else data[x]
        mock_indent_new_lines.side_effect = lambda x, _: x

        self.assertEqual(
            self.code_generator_instance.generate_code(st.CompositeSnippet(
                st.SimpleSnippet('for'),
                '>',
                st.SimpleSnippet('pass')
            )),
            'for item in collection:\n\t  \t pass'
        )

        mock_indent_new_lines.assert_called_once_with('pass', '\t  \t ')


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
