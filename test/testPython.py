from test.stdlib_test import TestStdlib


class TestC(TestStdlib):
    def setUp(self):
        self.language = "Python"

    def testFlow(self):
        self.verifySingleSnippet("forin$i%collection>pass", """
for i in collection:
\tpass
\t[{cursor_marker}]
""")

        self.verifySingleSnippet("for$i%collection>pass", """
for i in collection:
\tpass
\t[{cursor_marker}]
""")

        self.verifySingleSnippet("if$i is None>pass<elif$i==0>return 3<else>return 2", """
if i is None:
\tpass
elif i==0:
\treturn 3
else:
\treturn 2
\t[{cursor_marker}]
""")

        self.verifySingleSnippet("while$True>pass", """
while True:
\tpass
\t[{cursor_marker}]
""")

    def testObject(self):
        self.verifySingleSnippet("class!A:B>pass", """
class A(B):
\tpass

\t[{cursor_marker}]
""")

        self.verifySingleSnippet("class!A>method@foo$i>pass", """
class A:
\tdef foo(self, i):
\t\tpass
\t\t[{cursor_marker}]
""")

        self.verifySingleSnippet("class!A>smethod@foo$i>pass", """
class A:
\t@staticmethod
\tdef foo(i):
\t\tpass
\t\t[{cursor_marker}]
""")

        self.verifySingleSnippet("class!A>cmethod@foo$i>pass", """
class A:
\t@classmethod
\tdef foo(cls, i):
\t\tpass
\t\t[{cursor_marker}]
""")

        self.verifySingleSnippet("class!A>constr$i>pass", """
class A:
\tdef __init__(self, i):
\t\tpass
\t\t[{cursor_marker}]
""")

        self.verifySingleSnippet("func@a$i>pass", """
def a(i):
\tpass
\t[{cursor_marker}]
""")

    def testMain(self):
        self.verifySingleSnippet("[[main]]>pass", """
if __name__ == "__main__":
	pass
\t[{cursor_marker}]
""")
