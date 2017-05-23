from unittest import TestCase

from homotopy.parser import parser
from homotopy.syntax_tree import SimpleSnippet, CompositeSnippet


class TestParser(TestCase):
    def test_basic(self):
        self.assertEqual(parser.parse('asd'), SimpleSnippet('asd'))

    def test_left_associativity(self):
        left = '!@#'
        for l in left:
            self.assertEqual(parser.parse('first{0}second{0}third'.format(l)),
                             CompositeSnippet(
                                 CompositeSnippet(SimpleSnippet('first'), l,
                                                  SimpleSnippet('second')), l,
                                 SimpleSnippet('third'))
                             )

    def test_right_associativity(self):
        right = '$%:'
        for r in right:
            self.assertEqual(parser.parse('first{0}second{0}third'.format(r)),
                             CompositeSnippet(SimpleSnippet('first'), r,
                                              CompositeSnippet(SimpleSnippet('second'), r,
                                                               SimpleSnippet('third'))
                                              )
                             )
