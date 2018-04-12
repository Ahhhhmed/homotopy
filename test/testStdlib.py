from unittest import TestCase

from homotopy import parser, compiler


class TestStdlib(TestCase):
    def singleSnippet(self, snippet, expected_output):
        compiled_snippet = compiler.Compiler().compile(parser.parser.parse(snippet))

        self.assertEqual(expected_output.strip(), compiled_snippet)

    def testCpp(self):
        self.singleSnippet("for#int$i%n", """
for(int i; i<n; i++){

}
        """)

        self.singleSnippet('for#int$i%n>printf("hello");', """
for(int i; i<n; i++){
\tprintf("hello");
}
                """)

        self.singleSnippet('if#i==3>return 5;', """
if(i==3){
\treturn 5;
}

""")
        self.singleSnippet('forr#int$i%n>printf("hello");', """
for(int i=n; i>=0; i--){
\tprintf("hello");
}
""")
        self.singleSnippet('forin$item%collection>printf("hello");', """
for(auto&& item: collection){
\tprintf("hello");
}
""")
        self.singleSnippet('switch$i>case$1>asd<case$2>dsa', """
switch(i){
\tcase 1:
\tasd
\tbreak;
\tcase 2:
\tdsa
\tbreak;
}
""")
        self.singleSnippet('struct#A:B', """
struct A: public B {

};
""")
        self.singleSnippet('class#A%B>blah', """
class A: protected B {
\tblah
};
""")
        self.singleSnippet('class#A~B>func#void$foo#int$a#int$b', """
class A: private B {
\tvoid foo(int a, int b){

}
};
""")

