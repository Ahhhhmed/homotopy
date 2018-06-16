from test.stdlib_test import TestStdlib


class TestJS(TestStdlib):
    def setUp(self):
        self.language = "JavaScript"

    def testFlow(self):
        self.verifySingleSnippet("forin$x%collection>command<", """
for(let x of collection){
\tcommand
}
[{cursor_marker}]
""")

        self.verifySingleSnippet("forof$x%collection>command<", """
for(let x of collection){
\tcommand
}
[{cursor_marker}]
""")

    def testJson(self):
        self.verifySingleSnippet("dict>key$k1>value1<key$k2>value2<<", """
{
\tk1: value1,
\tk2: value2
}
[{cursor_marker}]
""")

        self.verifySingleSnippet("dict>k$k1>value1<k$k2>value2<<", """
{
\t"k1": value1,
\t"k2": value2
}
[{cursor_marker}]
""")

        self.verifySingleSnippet("dict1>key$k1>value1<key$k2>value2<<", """
{k1: value1, k2: value2}
[{cursor_marker}]
""")

        self.verifySingleSnippet("dict>key$k1>dict>key$nested>val<<<key$k2>value2<<", """
{
\tk1: {
\t\tnested: val
\t},
\tk2: value2
}
[{cursor_marker}]
""")

        self.verifySingleSnippet("dict>key$k1>dict>key$nested$val<<key$k2$value2<", """
{
\tk1: {
\t\tnested: val
\t},
\tk2: value2
}
[{cursor_marker}]
""")

        self.verifySingleSnippet("array>item1&item2<", """
[
\titem1,
\titem2
]
[{cursor_marker}]
""")

        self.verifySingleSnippet("array1>item1&item2<", """
[item1, item2]
[{cursor_marker}]
""")

    def testClass(self):
        self.verifySingleSnippet("class!A", """
class A {

}
[{cursor_marker}]
""")

        self.verifySingleSnippet("class!A:B>constr$a$b<", """
class A extends B {
\tconstructor(a, b){

\t}
}
[{cursor_marker}]
""")

        self.verifySingleSnippet("class!A:B>constr1$a$b<", """
class A extends B {
\tconstructor(a, b){ }
}
[{cursor_marker}]
""")

        self.verifySingleSnippet("class!A:B>method@met$a$b<", """
class A extends B {
\tmet(a, b){

\t}
}
[{cursor_marker}]
""")

        self.verifySingleSnippet("class!A:B>method1@met$a$b<", """
class A extends B {
\tmet(a, b){ }
}
[{cursor_marker}]
""")

    def testFunc(self):
        self.verifySingleSnippet("func@foo$i$j>return i+j<", """
function foo(i, j){
\treturn i+j
}
[{cursor_marker}]
""")

        self.verifySingleSnippet("func$i$j>return i+j<", """
function (i, j){
\treturn i+j
}
[{cursor_marker}]
""")

        self.verifySingleSnippet("f$i$j>i+j<", """
function (i, j){ return i+j; }
[{cursor_marker}]
""")

        self.verifySingleSnippet("func1$i$j>return i+j<", """
function (i, j){ return i+j }
[{cursor_marker}]
""")

        self.verifySingleSnippet("arrow$i$j>return i+j<", """
(i, j) => {
\treturn i+j
}
[{cursor_marker}]
""")

        self.verifySingleSnippet("a$i$j>i+j<", """
(i, j) => i+j
[{cursor_marker}]
""")

        self.verifySingleSnippet("arrow1$i$j>return i+j<", """
(i, j) => { return i+j }
[{cursor_marker}]
""")

    def testLetVar(self):
        self.verifySingleSnippet("let$x$3", """
let x = 3;
[{cursor_marker}]
""")

        self.verifySingleSnippet("let$x>3<", """
let x = 3;
[{cursor_marker}]
""")

        self.verifySingleSnippet("var$x$3", """
var x = 3;
[{cursor_marker}]
""")

        self.verifySingleSnippet("var$x>3<", """
var x = 3;
[{cursor_marker}]
""")
