from unittest import TestCase

from homotopy import homotopy


class TestStdlib(TestCase):
    def singleSnippet(self, snippet, expected_output):
        homotopy_instance = homotopy.Homotopy("c++")
        homotopy_instance.enable_cursor_marker()

        compiled_snippet = homotopy_instance.compile(snippet)

        self.assertEqual(expected_output.lstrip('\n').rstrip(), compiled_snippet)

    def testCpp(self):
        self.singleSnippet("for#int$i%0%n", """
for(int i=0; i<n; i++){

}
[{cursor_marker}]
""")

        self.singleSnippet("for#int$i%0%n>", """
for(int i=0; i<n; i++){
\t[{cursor_marker}]
}
""")

        self.singleSnippet('for#int$i%0%n>printf("hello");', """
for(int i=0; i<n; i++){
\tprintf("hello");
\t[{cursor_marker}]
}
                """)

        self.singleSnippet('if$i==3>return 5;', """
if(i==3){
\treturn 5;
\t[{cursor_marker}]
}
""")
        self.singleSnippet('while$i==3>return 5;', """
while(i==3){
\treturn 5;
\t[{cursor_marker}]
}

""")
        self.singleSnippet('forr#int$i%n%0>printf("hello");', """
for(int i=n; i>=0; i--){
\tprintf("hello");
\t[{cursor_marker}]
}
""")
        self.singleSnippet('forr#int$i%n%0>printf("hello");<', """
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
\t\tasd
\t\tbreak;

\tcase 2:
\t\tdsa
\t\t[{cursor_marker}]
\t\tbreak;
}
""")
        self.singleSnippet('switch$i>case$1>asd<case$2>dsa<<', """
switch(i){
\tcase 1:
\t\tasd
\t\tbreak;

\tcase 2:
\t\tdsa
\t\tbreak;
}
[{cursor_marker}]
""")
        self.singleSnippet('switch$i>case$1>asd<case$2>dsa<', """
switch(i){
\tcase 1:
\t\tasd
\t\tbreak;

\tcase 2:
\t\tdsa
\t\tbreak;

\t[{cursor_marker}]
}
""")
        self.singleSnippet('struct!A%public:B>', """
struct A: public B {
\t[{cursor_marker}]
};
""")
        self.singleSnippet('struct!A:B:C%public>', """
struct A: public B, public C {
\t[{cursor_marker}]
};
""")
        self.singleSnippet('class!A%protected:B%public:C>blah', """
class A: protected B, public C {
\tblah

\t[{cursor_marker}]
};
""")
        self.singleSnippet('class!A>constr#int$i&constr#int$i#int$j', """
class A {
\tpublic: A(int i){

\t}

\tpublic: A(int i, int j){

\t}

\t[{cursor_marker}]
};
""")
        self.singleSnippet('class!A%public:B>pconstr#int$i', """
class A: public B {
\tprivate: A(int i){

\t}

\t[{cursor_marker}]
};
""")
        self.singleSnippet('class!A%public:B>econstr#int$i', """
class A: public B {
\tpublic: A(int i){}

\t[{cursor_marker}]
};
""")
        self.singleSnippet('class!A%public:B>epconstr#int$i', """
class A: public B {
\tprivate: A(int i){}

\t[{cursor_marker}]
};
""")
        self.singleSnippet('class!A%public:B>niconstr#int$i', """
class A: public B {
\tpublic: A(int i);

\t[{cursor_marker}]
};
""")
        self.singleSnippet('class!A%public:B>nipconstr#int$i', """
class A: public B {
\tprivate: A(int i);

\t[{cursor_marker}]
};
""")
        self.singleSnippet('class!A%public:B>pconstr#int$i&method#void@test#int$value', """
class A: public B {
\tprivate: A(int i){

\t}

\tpublic: void test(int value){

\t}

\t[{cursor_marker}]
};
""")
        self.singleSnippet('class!A%public:B>pconstr#int$i>// c++ comment<pmethod#int@five>return 5', """
class A: public B {
\tprivate: A(int i){
\t\t// c++ comment
\t}

\tprivate: int five(){
\t\treturn 5

\t\t[{cursor_marker}]
\t}
};
""")
        self.singleSnippet('class!A%public:B>amethod#void@name', """
class A: public B {
\tpublic: void name() = 0;

\t[{cursor_marker}]
};
""")
        self.singleSnippet('  class!A%public:B>apmethod#void@name', """
  class A: public B {
  \tprivate: void name() = 0;

  \t[{cursor_marker}]
  };
""")
        self.singleSnippet('  class!A%public:B>amethod#void@name', """
  class A: public B {
  \tpublic: void name() = 0;

  \t[{cursor_marker}]
  };
""")
        self.singleSnippet('  class!A%public:B>nimethod#void@name', """
  class A: public B {
  \tpublic: void name();

  \t[{cursor_marker}]
  };
""")
        self.singleSnippet('  class!A%public:B>nipmethod#void@name', """
  class A: public B {
  \tprivate: void name();

  \t[{cursor_marker}]
  };
""")
        self.singleSnippet('class!A%public:B>[[singleton]]', """
class A: public B {
\tpublic: A& getInstance(){
\t\tstatic A instance;

\t\treturn instance
\t}

\tprivate: A(){}
\tprivate: A(A const& origin);
\tprivate: void operator=(A const& origin);

\t[{cursor_marker}]
};
""")
        self.singleSnippet('class!Composite:Component%public>[[compositeclass]]&pmethod#void@traverse[[compositemethod]]', """
class Composite: public Component {
\tprivate: std::vector<Component*> children;

\tpublic: void add(Component *item){
\t\tchildren.puch_back(item);
\t}

\tprivate: void traverse(){
\t\tfor(int i=0; i<children.size(); i++){
\t\t\t\tchildren[i]->traverse();
\t\t\t}
\t}

\t[{cursor_marker}]
};
""")
        self.singleSnippet('enum1!deca>pera&mika = 2&zika = 3', """
enum deca { pera, mika = 2, zika = 3, [{cursor_marker}] };
""")
        self.singleSnippet('enum1!deca>pera&mika = 2&zika = 3<', """
enum deca { pera, mika = 2, zika = 3 };
[{cursor_marker}]
""")
        self.singleSnippet('enum!deca>pera&mika = 2&zika = 3<', """
enum deca {
\tpera,
\tmika = 2,
\tzika = 3
};
[{cursor_marker}]
""")
        self.singleSnippet('template^T>class!A', """
template <class T>
class A {

};

[{cursor_marker}]
""")
        self.singleSnippet('constri!A#int$i', """
A::A(int i){

}
[{cursor_marker}]
""")
        self.singleSnippet('methodi!A#void@pera#int$i', """
void A::pera(int i){

}
[{cursor_marker}]
""")
