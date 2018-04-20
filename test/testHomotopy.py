from unittest import TestCase
from unittest.mock import patch, MagicMock

from homotopy.homotopy import Homotopy


class TestHomotopy(TestCase):
    def setUp(self):
        self.homotopy_instance = Homotopy("c++")

    def test_init(self):
        self.assertEqual([], self.homotopy_instance.user_path)
        self.assertEqual('\t', self.homotopy_instance.indent)
        self.assertEqual(False, self.homotopy_instance.put_cursor_marker)
        self.assertEqual("c++", self.homotopy_instance.language)

    def test_add_lib_folder(self):
        self.homotopy_instance.add_lib_folder("test_folder1")
        self.assertEqual(["test_folder1"], self.homotopy_instance.user_path)

        self.homotopy_instance.add_lib_folder("test_folder2")
        self.assertEqual(["test_folder1", "test_folder2"], self.homotopy_instance.user_path)

    def test_clear_user_lib(self):
        self.homotopy_instance.add_lib_folder("test_folder1")
        self.homotopy_instance.clear_user_lib()
        self.assertEqual([], self.homotopy_instance.user_path)

        self.homotopy_instance.add_lib_folder("test_folder1")
        self.homotopy_instance.add_lib_folder("test_folder2")
        self.homotopy_instance.clear_user_lib()
        self.assertEqual([], self.homotopy_instance.user_path)

    def test_set_indent(self):
        self.homotopy_instance.set_indent("test")
        self.assertEqual("test", self.homotopy_instance.indent)

    def test_enable_cursor_marker(self):
        self.homotopy_instance.enable_cursor_marker()
        self.assertEqual(True, self.homotopy_instance.put_cursor_marker)

    def test_disable_cursor_marker(self):
        self.homotopy_instance.disable_cursor_marker()
        self.assertEqual(False, self.homotopy_instance.put_cursor_marker)

    def test_set_language(self):
        self.homotopy_instance.set_language("python")
        self.assertEqual("python", self.homotopy_instance.language)

    @patch('homotopy.preprocessor.Preprocessor.__init__')
    @patch('homotopy.preprocessor.Preprocessor.expand_decorators')
    @patch('homotopy.preprocessor.Preprocessor.put_cursor_marker')
    @patch('homotopy.parser.Parser.__init__')
    @patch('homotopy.parser.Parser.parse')
    @patch('homotopy.compiler.Compiler.__init__')
    @patch('homotopy.compiler.Compiler.compile')
    @patch('homotopy.snippet_provider.SnippetProvider')
    @patch('homotopy.util.IndentManager')
    def test_compile(
            self,
            mock_indent_manager,
            mock_provider,
            compile_method,
            compile_init,
            parser_parse,
            parser_init,
            preprocessor_put_cursor_marker,
            preprocessor_expand_decorators,
            preprocessor_init,
    ):
        mock_indent_manager_instance = MagicMock()
        mock_indent_manager_instance.take_base_indent = MagicMock(side_effect=lambda x: x)
        mock_indent_manager_instance.indent_base = MagicMock(side_effect=lambda x: x)
        mock_indent_manager.return_value = mock_indent_manager_instance
        mock_provider.return_value = "mock_provider"
        compile_method.return_value = "compile_method_output"
        compile_init.return_value = None
        parser_parse.return_value = "parse_method_output"
        parser_init.return_value = None
        preprocessor_put_cursor_marker.return_value = "put_cursor_marker_output"
        preprocessor_expand_decorators.return_value = "expand_decorators_output"
        preprocessor_init.return_value = None

        self.homotopy_instance.enable_cursor_marker()
        self.homotopy_instance.add_lib_folder("test_folder")

        self.assertEqual("compile_method_output", self.homotopy_instance.compile("test_snippet"))

        mock_provider.assert_called_once_with("c++", ["test_folder", Homotopy.stdlib_path])
        compile_method.assert_called_once_with("parse_method_output")
        compile_init.assert_called_once_with("mock_provider", mock_indent_manager_instance)
        parser_parse.assert_called_once_with("put_cursor_marker_output")
        parser_init.assert_called_once_with()
        preprocessor_put_cursor_marker.assert_called_once_with("expand_decorators_output")
        preprocessor_expand_decorators.assert_called_once_with("test_snippet")
        preprocessor_init.assert_called_once_with("mock_provider")
        mock_indent_manager_instance.take_base_indent.assert_called_once_with("test_snippet")
        mock_indent_manager_instance.indent_base.assert_called_once_with("compile_method_output")
