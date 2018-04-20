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
blah
[{cursor_marker}]
};
""")

        self.singleSnippet('class!A>public>constr#int$i&constr#int$i#int$j', """
class A {
public:
\tA(int i){

\t}

\tA(int i, int j){

\t}

\t[{cursor_marker}]
};
""")

        self.singleSnippet('class!A%public:B>private>constr#int$i', """
class A: public B {
private:
\tA(int i){

\t}

\t[{cursor_marker}]
};
""")

        self.singleSnippet('class!A%public:B>public>econstr#int$i', """
class A: public B {
public:
\tA(int i){}

\t[{cursor_marker}]
};
""")

        self.singleSnippet('class!A%public:B>public>niconstr#int$i', """
class A: public B {
public:
\tA(int i);

\t[{cursor_marker}]
};
""")

        self.singleSnippet('class!A%public:B>private>constr#int$i<public>method#void@test#int$value', """
class A: public B {
private:
\tA(int i){

\t}
public:
\tvoid test(int value){

\t}

\t[{cursor_marker}]
};
""")

        self.singleSnippet('class!A%public:B>public>amethod#void@name', """
class A: public B {
public:
\tvoid name() = 0;

\t[{cursor_marker}]
};
""")

        self.singleSnippet('  class!A%public:B>public>amethod#void@name', """
  class A: public B {
  public:
  \tvoid name() = 0;

  \t[{cursor_marker}]
  };
""")

        self.singleSnippet('  class!A%public:B>public>nimethod#void@name', """
  class A: public B {
  public:
  \tvoid name();

  \t[{cursor_marker}]
  };
""")

        self.singleSnippet('  class!A%public:B>private>nimethod#void@name', """
  class A: public B {
  private:
  \tvoid name();

  \t[{cursor_marker}]
  };
""")

        self.singleSnippet('class!A%public:B>[[singleton]]', """
class A: public B {
public:
\tA& getInstance(){
\t\tstatic A instance;

\t\treturn instance
\t}
private:
\tA(){}
\tA(A const& origin);
\tvoid operator=(A const& origin);

\t[{cursor_marker}]
};
""")

        self.singleSnippet('class!Composite:Component%public>[[compositeclass]]public>method#void@traverse[[compositemethod]]', """
class Composite: public Component {
public:
\tvoid add(Component *item){
\t\tchildren.puch_back(item);
\t}
private:
\tstd::vector<Component*> children;
public:
\tvoid traverse(){
\t\tfor(int i=0; i<children.size(); i++){
\t\t\tchildren[i]->traverse();
\t\t}
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

        self.singleSnippet('constri1!A#int$i', """
A::A(int i){

}
[{cursor_marker}]
""")

        self.singleSnippet('methodi1!A#void@pera#int$i', """
void A::pera(int i){

}
[{cursor_marker}]
""")

        self.singleSnippet('wblock!A>constri&constri$i$j#int&methodi#void@nothing', """
A::A(){

}

A::A(int i, int j){

}

void A::nothing(){

}

[{cursor_marker}]
""")

        self.singleSnippet('if$one>if$two>if$3', """
if(one){
\tif(two){
\t\tif(3){

\t\t}
\t\t[{cursor_marker}]
\t}
}
""")

        self.singleSnippet('class!A>public>dconstr#int$i', """
class A {
public:
\tA(int i) = delete;

\t[{cursor_marker}]
};
""")

        self.singleSnippet('class!A>public>dmethod@nothing#void#int$i', """
class A {
public:
\tvoid nothing(int i) = delete;

\t[{cursor_marker}]
};
""")
