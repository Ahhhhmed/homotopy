from unittest import TestCase

from homotopy.util import ContextManager, IndentManager


class TestIndentManager(TestCase):
    def setUp(self):
        self.indent_manager_instance = IndentManager()

    def test_init(self):
        self.assertEqual("", self.indent_manager_instance.base_indent)

        self.assertEqual("indent", IndentManager("indent").base_indent)

    def test_indent_new_lines(self):
        self.assertEqual("test", self.indent_manager_instance.indent_new_lines("test", "indent "))

        self.assertEqual("line1\nindent line2",
                         self.indent_manager_instance.indent_new_lines("line1\nline2", "indent "))

        self.assertEqual(
            "line1\nindent line2\nindent line3",
            self.indent_manager_instance.indent_new_lines("line1\nline2\nline3", "indent "))

        self.assertEqual("line1\nindent line2",
                         self.indent_manager_instance.indent_new_lines("line1\nline2\n", "indent "))

        self.assertEqual("line1\nindent line2\n",
                         self.indent_manager_instance.indent_new_lines("line1\nline2\n\n", "indent "))

        self.assertEqual("line1\nindent line2\n",
                         self.indent_manager_instance.indent_new_lines("line1\nline2\n  \n", "indent "))

        self.assertEqual(
            "\nindent line1\nindent line2",
            self.indent_manager_instance.indent_new_lines("\nline1\nline2", "indent "))

    def test_indent_base(self):
        self.indent_manager_instance.base_indent = "indent "

        self.assertEqual("indent test", self.indent_manager_instance.indent_base("test"))
        self.assertEqual("indent line1\nindent line2", self.indent_manager_instance.indent_base("line1\nline2"))

        self.assertEqual(
            "indent line1\nindent line2\nindent line3",
            self.indent_manager_instance.indent_base("line1\nline2\nline3"))

        self.assertEqual("indent line1\nindent line2", self.indent_manager_instance.indent_base("line1\nline2\n"))
        self.assertEqual("indent line1\nindent line2\n", self.indent_manager_instance.indent_base("line1\nline2\n\n"))
        self.assertEqual("indent line1\nindent line2\n", self.indent_manager_instance.indent_base("line1\nline2\n  \n"))

        self.assertEqual(
            "\nindent line1\nindent line2",
            self.indent_manager_instance.indent_base("\nline1\nline2"))

    def test_take_base_indent(self):
        self.assertEqual("", self.indent_manager_instance.take_base_indent("   "))
        self.assertEqual("   ", self.indent_manager_instance.base_indent)

        self.assertEqual("for", self.indent_manager_instance.take_base_indent("   for"))
        self.assertEqual("   ", self.indent_manager_instance.base_indent)

        self.assertEqual("for", self.indent_manager_instance.take_base_indent("\tfor"))
        self.assertEqual("\t", self.indent_manager_instance.base_indent)

        self.assertEqual("for", self.indent_manager_instance.take_base_indent("\t  \t for"))
        self.assertEqual("\t  \t ", self.indent_manager_instance.base_indent)


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
