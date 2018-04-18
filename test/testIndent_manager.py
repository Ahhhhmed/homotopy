from unittest import TestCase
from homotopy.indent_manager import IndentManager


class TestIndentManager(TestCase):
    def setUp(self):
        self.indent_manager_instance = IndentManager()

    def test_init(self):
        self.assertEqual("", self.indent_manager_instance.base_indent)
        self.assertEqual([], self.indent_manager_instance.indent_stack)

        self.assertEqual("indent", IndentManager("indent").base_indent)

    def test_push_indent(self):
        self.indent_manager_instance.push_indent("level1")
        self.assertEqual(["level1"], self.indent_manager_instance.indent_stack)

        self.indent_manager_instance.push_indent("level2")
        self.assertEqual(["level1", "level2"], self.indent_manager_instance.indent_stack)

    def test_pop_indent(self):
        self.indent_manager_instance.push_indent("level1")
        self.indent_manager_instance.push_indent("level2")

        self.indent_manager_instance.pop_indent()
        self.assertEqual(["level1"], self.indent_manager_instance.indent_stack)

        self.indent_manager_instance.pop_indent()
        self.assertEqual([], self.indent_manager_instance.indent_stack)

        self.indent_manager_instance.pop_indent()
        self.assertEqual([], self.indent_manager_instance.indent_stack)

    def test_get_current_indent(self):
        self.indent_manager_instance.push_indent("level1")
        self.indent_manager_instance.push_indent("level2")

        self.assertEqual("level1level2", self.indent_manager_instance.get_current_indent())

        self.indent_manager_instance.pop_indent()
        self.assertEqual("level1", self.indent_manager_instance.get_current_indent())

        self.indent_manager_instance.pop_indent()
        self.assertEqual("", self.indent_manager_instance.get_current_indent())

        self.indent_manager_instance.pop_indent()
        self.assertEqual("", self.indent_manager_instance.get_current_indent())

    def test_indent_new_lines(self):
        self.indent_manager_instance.push_indent("indent ")

        self.assertEqual("test", self.indent_manager_instance.indent_new_lines("test"))
        self.assertEqual("line1\nindent line2", self.indent_manager_instance.indent_new_lines("line1\nline2"))

        self.assertEqual(
            "line1\nindent line2\nindent line3",
            self.indent_manager_instance.indent_new_lines("line1\nline2\nline3"))

        self.assertEqual("line1\nindent line2", self.indent_manager_instance.indent_new_lines("line1\nline2\n"))
        self.assertEqual("line1\nindent line2\n", self.indent_manager_instance.indent_new_lines("line1\nline2\n\n"))
        self.assertEqual("line1\nindent line2\n", self.indent_manager_instance.indent_new_lines("line1\nline2\n  \n"))

        self.assertEqual(
            "\nindent line1\nindent line2",
            self.indent_manager_instance.indent_new_lines("\nline1\nline2"))

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
