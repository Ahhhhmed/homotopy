from unittest import TestCase

from homotopy.parser import Parser
from homotopy.syntax_tree import SimpleSnippet, CompositeSnippet


class TestParser(TestCase):
    def setUp(self):
        self.parser_instance = Parser()

    def test_basic(self):
        self.assertEqual(self.parser_instance.parse(''), SimpleSnippet(''))

        self.assertEqual(self.parser_instance.parse('asd'), SimpleSnippet('asd'))
        self.assertEqual(self.parser_instance.parse('asd#'), CompositeSnippet(SimpleSnippet('asd'), '#', SimpleSnippet('')))
        self.assertEqual(self.parser_instance.parse('asd!#1'),
                         CompositeSnippet(
                             CompositeSnippet(SimpleSnippet('asd'), '!',
                                              SimpleSnippet('')), '#',
                             SimpleSnippet('1'))
                         )

    def test_parameters(self):
        operators = '!@#$%:~^'
        for l in operators:
            self.assertEqual(self.parser_instance.parse('first{0}second{0}third'.format(l)),
                             CompositeSnippet(
                                 CompositeSnippet(SimpleSnippet('first'), l,
                                                  SimpleSnippet('second')), l,
                                 SimpleSnippet('third'))
                             )

    def test_into(self):
        self.assertEqual(self.parser_instance.parse('asd>dsa'), CompositeSnippet(SimpleSnippet('asd'), '>', SimpleSnippet('dsa')))
        self.assertEqual(self.parser_instance.parse('asd>dsa#2'),
                         CompositeSnippet(SimpleSnippet('asd'), '>',
                                          CompositeSnippet(SimpleSnippet('dsa'), '#',
                                                           SimpleSnippet('2')))
                         )

        self.assertEqual(self.parser_instance.parse('for>if&if'),
                         CompositeSnippet(
                             CompositeSnippet(SimpleSnippet('for'), '>',
                                              SimpleSnippet('if')), '>',
                             SimpleSnippet('if'))
                         )

        self.assertEqual(self.parser_instance.parse('for>if>if<if'),
                         CompositeSnippet(
                             CompositeSnippet(SimpleSnippet('for'), '>',
                                              CompositeSnippet(SimpleSnippet('if'), '>', SimpleSnippet('if'))), '>',
                             SimpleSnippet('if'))
                         )

        self.assertEqual(self.parser_instance.parse('for>if>if>if<<if'),
                         CompositeSnippet(
                             CompositeSnippet(SimpleSnippet('for'), '>',
                                              CompositeSnippet(SimpleSnippet('if'), '>',
                                                               CompositeSnippet(
                                                                   SimpleSnippet('if'), '>',
                                                               SimpleSnippet('if')))), '>',
                             SimpleSnippet('if'))
                         )

        self.assertEqual(self.parser_instance.parse('for>if#5>if<if'),
                         CompositeSnippet(
                             CompositeSnippet(SimpleSnippet('for'), '>',
                                              CompositeSnippet(
                                                  CompositeSnippet(SimpleSnippet('if'), '#', SimpleSnippet('5')), '>',
                                                  SimpleSnippet('if'))), '>',
                             SimpleSnippet('if'))
                         )

        self.assertEqual(self.parser_instance.parse('for&for'),
                         CompositeSnippet(
                             CompositeSnippet(
                                 SimpleSnippet('block'),
                                 '>',
                                 SimpleSnippet('for')),
                             '>',
                             SimpleSnippet('for')
                         ))

        self.assertEqual(self.parser_instance.parse('for>if<if'),
                         CompositeSnippet(
                             CompositeSnippet(
                                 SimpleSnippet('block'),
                                 '>',
                                 CompositeSnippet(
                                     SimpleSnippet('for'),
                                     '>',
                                     SimpleSnippet('if')
                                 )
                             ),
                             '>',
                             SimpleSnippet('if')
                         ))

    def test_escape(self):
        self.assertEqual(self.parser_instance.parse(r"i\>4"), SimpleSnippet("i>4"))
        self.assertEqual(self.parser_instance.parse("ignore\\"), SimpleSnippet("ignore"))

        self.assertEqual(self.parser_instance.parse(r"i\\>4"),
                         CompositeSnippet(
                             SimpleSnippet("i\\"),
                             '>',
                             SimpleSnippet("4")
                         )
                         )

        self.assertEqual(self.parser_instance.parse(r"if$i\>4"),
                         CompositeSnippet(
                             SimpleSnippet("if"),
                             '$',
                             SimpleSnippet("i>4")
                         ))
