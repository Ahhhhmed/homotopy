from unittest import TestCase

from homotopy import parser, compiler, preprocessor


class TestStdlib(TestCase):
    def singleSnippet(self, snippet, expected_output):
        compiled_snippet = compiler.Compiler().compile(
            parser.parser.parse(
                preprocessor.Preprocessor.put_cursor_marker(
                    preprocessor.Preprocessor.expand_decorators(snippet)))
        )

        self.assertEqual(expected_output.strip(), compiled_snippet)

    def testCpp(self):
        self.singleSnippet("for#int$i%n", """
for(int i; i<n; i++){

}
[{cursor_marker}]
""")

        self.singleSnippet("for#int$i%n>", """
for(int i; i<n; i++){
\t[{cursor_marker}]
}
""")

        self.singleSnippet('for#int$i%n>printf("hello");', """
for(int i; i<n; i++){
\tprintf("hello");
\t[{cursor_marker}]
}
                """)

        self.singleSnippet('if#i==3>return 5;', """
if(i==3){
\treturn 5;
\t[{cursor_marker}]
}

""")
        self.singleSnippet('forr#int$i%n>printf("hello");', """
for(int i=n; i>=0; i--){
\tprintf("hello");
\t[{cursor_marker}]
}
""")
        self.singleSnippet('forr#int$i%n>printf("hello");<', """
for(int i=n; i>=0; i--){
\tprintf("hello");
}
[{cursor_marker}]
""")

        self.singleSnippet('forin$item%collection>printf("hello");', """
for(auto&& item: collection){
\tprintf("hello");
\t[{cursor_marker}]
}
""")
        self.singleSnippet('switch$i>case$1>asd<case$2>dsa', """
switch(i){
\tcase 1:
\tasd
\tbreak;
\tcase 2:
\tdsa
\t[{cursor_marker}]
\tbreak;
}
""")
        self.singleSnippet('switch$i>case$1>asd<case$2>dsa<<', """
switch(i){
\tcase 1:
\tasd
\tbreak;
\tcase 2:
\tdsa
\tbreak;
}
[{cursor_marker}]
""")
        self.singleSnippet('struct#A:B>', """
struct A: public B {
\t[{cursor_marker}]
};
""")
        self.singleSnippet('class#A%B>blah', """
class A: protected B {
\tblah
\t[{cursor_marker}]
};
""")
        self.singleSnippet('class#A~B>func#void$foo#int$a#int$b', """
class A: private B {
\tvoid foo(int a, int b){

}
\t[{cursor_marker}]
};
""")

