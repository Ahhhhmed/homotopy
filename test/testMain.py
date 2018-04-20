from unittest import TestCase
from unittest.mock import patch, call

import homotopy.__main__


class TestMain(TestCase):
    @patch("homotopy.__main__.main")
    def test_init(self, mock_main):
        with patch("homotopy.__main__.__name__", "__main__"):
            homotopy.__main__.init()

        mock_main.assert_called_once_with()

    def test_main(self):
        with patch("homotopy.Homotopy.compile", return_value="") as mock_compile:
            with patch("sys.argv", ["testing", "c++", "invalid_snippet"]):
                homotopy.__main__.main()
            mock_compile.assert_called_once_with("invalid_snippet")

        with patch("homotopy.Homotopy.compile", return_value="") as mock_compile:
            with patch("homotopy.Homotopy.set_indent") as mock_set_indent:
                with patch("sys.argv", ["testing", "-t", "3", "c++", "invalid_snippet"]):
                    homotopy.__main__.main()

                mock_set_indent.assert_called_once_with("   ")
            mock_compile.assert_called_once_with("invalid_snippet")

        with patch("homotopy.Homotopy.compile", return_value="") as mock_compile:
            with patch("homotopy.Homotopy.enable_cursor_marker") as mock_enable_cursor_marker:
                with patch("sys.argv", ["testing", "-c", "c++", "invalid_snippet"]):
                    homotopy.__main__.main()

                mock_enable_cursor_marker.assert_called_once_with()
            mock_compile.assert_called_once_with("invalid_snippet")

        with patch("homotopy.Homotopy.compile", return_value="") as mock_compile:
            with patch("homotopy.Homotopy.add_lib_folder") as mock_add_lib_folder:
                with patch("sys.argv", ["testing", "-p", "user_folder", "c++", "invalid_snippet"]):
                    homotopy.__main__.main()

                mock_add_lib_folder.assert_called_once_with("user_folder")
            mock_compile.assert_called_once_with("invalid_snippet")

        with patch("homotopy.Homotopy.compile", return_value="") as mock_compile:
            with patch("homotopy.Homotopy.add_lib_folder") as mock_add_lib_folder:
                with patch("sys.argv", ["testing", "-p", "user_folder1:user_folder2", "c++", "invalid_snippet"]):
                    homotopy.__main__.main()

                mock_add_lib_folder.assert_has_calls([
                    call("user_folder1"),
                    call("user_folder2")
                ])
            mock_compile.assert_called_once_with("invalid_snippet")
