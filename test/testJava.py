from test.stdlib_test import TestStdlib


class TestC(TestStdlib):
    def setUp(self):
        self.language = "Java"

    def testFlow(self):
        self.verifySingleSnippet("forin#int$i%collection", """
for(int i: collection){

}
[{cursor_marker}]
""")

    def testObject(self):
        self.verifySingleSnippet("class!A:B~C~D", """
class A extends B implements C, D {

}
[{cursor_marker}]
""")

        self.verifySingleSnippet("class!A>method#void@nothing", """
class A {
\tpublic void nothing(){

\t}

\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet("class!A>method1#void@nothing", """
class A {
\tpublic void nothing(){ }

\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet("class!A>method1#int@five>return 5;", """
class A {
\tpublic int five(){ return 5; [{cursor_marker}] }
}
""")

        self.verifySingleSnippet("class!A>amethod#int@five", """
class A {
\tpublic abstract int five();

\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet("class!A>pmethod#void@nothing", """
class A {
\tprivate void nothing(){

\t}

\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet("class!A>pmethod1#void@nothing", """
class A {
\tprivate void nothing(){ }

\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet("class!A>pmethod1#int@five>return 5;", """
class A {
\tprivate int five(){ return 5; [{cursor_marker}] }
}
""")

        self.verifySingleSnippet("class!A>pamethod#int@five", """
class A {
\tprivate abstract int five();

\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet("class!A>promethod#void@nothing", """
class A {
\tprotected void nothing(){

\t}

\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet("class!A>promethod1#void@nothing", """
class A {
\tprotected void nothing(){ }

\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet("class!A>promethod1#int@five>return 5;", """
class A {
\tprotected int five(){ return 5; [{cursor_marker}] }
}
""")

        self.verifySingleSnippet("class!A>proamethod#int@five", """
class A {
\tprotected int abstract five();

\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet("class!A>constr#int$i", """
class A {
\tpublic A(int i){

\t}

\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet("class!A>constr1#int$i", """
class A {
\tpublic A(int i){ }

\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet("class!A>pconstr#int$i", """
class A {
\tprivate A(int i){

\t}

\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet("class!A>pconstr1#int$i", """
class A {
\tprivate A(int i){ }

\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet("class!A>proconstr#int$i", """
class A {
\tprotected A(int i){

\t}

\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet("class!A>proconstr1#int$i", """
class A {
\tprotected A(int i){ }

\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet("enum1!Color>red&green&blue<", """
enum Color { red, green, blue; }
[{cursor_marker}]
""")

    def testTemplate(self):
        self.verifySingleSnippet("class!A^T>method#void@nothing^K", """
class A<T> {
\tpublic void nothing<K>(){

\t}

\t[{cursor_marker}]
}
""")

    def testPatterns(self):

        self.verifySingleSnippet("class!A:B>[[compositeclass]]&method#void@nothing>[[compositemethod]]<", """
class A extends B {
\tprivate List<B> children = ArrayList<B>();
\tpublic void add(B item){
\t\tchildren.add(item);
\t}

\tpublic void nothing(){
\t\tfor(int i=0; i<children.size(); i++){
\t\t\tchildren[i].nothing();
\t\t}
\t}

\t[{cursor_marker}]
}
""")

    def testMain(self):
        self.verifySingleSnippet("class!A>[[main]]>return 0;<", """
class A {
\tpublic static void main(String[] args){
\t\treturn 0;
\t}

\t[{cursor_marker}]
}
""")


