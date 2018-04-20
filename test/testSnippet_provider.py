from unittest import TestCase
from unittest.mock import patch, MagicMock
from unittest.mock import mock_open

import os

import homotopy.snippet_provider as sp


class TestSnippetProvider(TestCase):
    def test_getitem(self):
        provider = sp.SnippetProvider("", [])

        provider.data = {
            "for": "for # in !:\n\tpass"
        }

        self.assertEqual(provider['for'], "for # in !:\n\tpass")
        self.assertEqual(provider['i==5'], "i==5")

    @patch('os.listdir')
    def test_initialization(self, listdir):
        listdir.return_value = ['test.json', 'test.txt']

        self.assertDictEqual(sp.SnippetProvider("", []).data, {}, "Snippet provider should be empty.")

        with patch('builtins.open',
                   mock_open(read_data='[{"name": "for","language": "C++","snippet": "if(#){$}"}]')) as m:
            provider = sp.SnippetProvider("c++", ["test"])

            self.assertEqual("if(#){$}", provider["for"])

            m.assert_called_once_with(os.path.join("test", "test.json"))

            listdir.assert_called_once_with("test")

        with patch('builtins.open',
                   mock_open(read_data='[{"name": "for","language": "C++","snippet": "if(#){$}"}]')) as m:
            provider = sp.SnippetProvider("java", ["test"])

            self.assertEqual("for", provider["for"])

        with patch('logging.warning', MagicMock()) as m:
            with patch('builtins.open', mock_open()) as m_open:
                m_open.side_effect = IOError()

                provider = sp.SnippetProvider("c++", ["test"])

                m.assert_called_once_with("Could not get data from file test.json", exc_info=True)

        with patch('logging.warning', MagicMock()) as m:
            with patch('builtins.open', mock_open(read_data='invalidJSON')) as m_open:
                provider = sp.SnippetProvider("c++", ["test"])

                m.assert_called_once_with("Could not get data from file test.json", exc_info=True)

        with patch('logging.warning', MagicMock()) as m:
            with patch('builtins.open', mock_open(
                read_data='[{"name": "for","language": "C++","snippet": "if(#){$}"}' 
                          ',{"name": "for","language": "C++","snippet": "if(#){$}"}]')) as m_open:
                provider = sp.SnippetProvider("c++", ["test"])

                m.assert_called_once_with("Multiple definition for for")

        with patch('builtins.open',
                   mock_open(read_data='[{"name": "for","language": ["C++", "java"],"snippet": "if(#){$}"}]')) as m:
            provider = sp.SnippetProvider("c++", ["test"])

            self.assertEqual("if(#){$}", provider["for"])

        with patch('builtins.open',
                   mock_open(read_data='[{"name": "for","language": ["all"],"snippet": "if(#){$}"}]')) as m:
            provider = sp.SnippetProvider("c++", ["test"])

            self.assertEqual("if(#){$}", provider["for"])

        with patch('builtins.open',
                   mock_open(read_data='[{"name": "for","language": ["~C++"],"snippet": "if(#){$}"}]')) as m:
            provider = sp.SnippetProvider("c++", ["test"])

            self.assertEqual("for", provider["for"])

        with patch('builtins.open',
                   mock_open(read_data='[{"name": "for","language": ["C++", "~C++"],"snippet": "if(#){$}"}]')) as m:
            provider = sp.SnippetProvider("c++", ["test"])

            self.assertEqual("for", provider["for"])

        with patch('builtins.open',
                   mock_open(read_data='[{"name": "for","language": ["all", "~C++"],"snippet": "if(#){$}"}]')) as m:
            provider = sp.SnippetProvider("c++", ["test"])

            self.assertEqual("for", provider["for"])
