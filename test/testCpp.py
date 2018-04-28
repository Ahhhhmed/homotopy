from test.stdlib_test import TestStdlib


class TestCpp(TestStdlib):
    def setUp(self):
        self.language = "c++"

    def testFlow(self):
        self.verifySingleSnippet("for#int$i%0%n", """
for(int i=0; i<n; i++){

}
[{cursor_marker}]
""")

        self.verifySingleSnippet("for#int$i%0%n>", """
for(int i=0; i<n; i++){
\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet('for#int$i%0%n>printf("hello");', """
for(int i=0; i<n; i++){
\tprintf("hello");
\t[{cursor_marker}]
}
                """)

        self.verifySingleSnippet('if$i==3>return 5;', """
if(i==3){
\treturn 5;
\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet('if$i==2>return 4;<else>return 3;', """
if(i==2){
\treturn 4;
}
else {
\treturn 3;
\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet('while$i==3>return 5;', """
while(i==3){
\treturn 5;
\t[{cursor_marker}]
}

""")

        self.verifySingleSnippet('forr#int$i%n%0>printf("hello");', """
for(int i=n; i>=0; i--){
\tprintf("hello");
\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet('forr#int$i%n%0>printf("hello");<', """
for(int i=n; i>=0; i--){
\tprintf("hello");
}
[{cursor_marker}]
""")


        self.verifySingleSnippet('forin#auto\&\&$item%collection>printf("hello");', """
for(auto&& item: collection){
\tprintf("hello");
\t[{cursor_marker}]
}
""")

        self.verifySingleSnippet('switch$i>case$1>asd<case$2>dsa', """
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

        self.verifySingleSnippet('switch$i>case$1$2>printf("one or two");', """
switch(i){
\tcase 1:
\tcase 2:
\t\tprintf("one or two");
\t\t[{cursor_marker}]
\t\tbreak;
}
""")

        self.verifySingleSnippet('switch$i>case$1>asd<case$2>dsa<<', """
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

        self.verifySingleSnippet('switch$i>case$1>asd<case$2>dsa<', """
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

    def testObjects(self):
        self.verifySingleSnippet('struct!A%public:B>', """
struct A: public B {
\t[{cursor_marker}]
};
""")

        self.verifySingleSnippet('struct!A:B:C%public>', """
struct A: public B, public C {
\t[{cursor_marker}]
};
""")

        self.verifySingleSnippet('class!A%protected:B%public:C>blah', """
class A: protected B, public C {
blah
[{cursor_marker}]
};
""")

        self.verifySingleSnippet('class!A>public>constr#int$i&constr#int$i#int$j', """
class A {
public:
\tA(int i){

\t}

\tA(int i, int j){

\t}

\t[{cursor_marker}]
};
""")

        self.verifySingleSnippet('class!A%public:B>private>constr#int$i', """
class A: public B {
private:
\tA(int i){

\t}

\t[{cursor_marker}]
};
""")

        self.verifySingleSnippet('class!A%public:B>public>econstr#int$i', """
class A: public B {
public:
\tA(int i){}

\t[{cursor_marker}]
};
""")

        self.verifySingleSnippet('class!A%public:B>public>niconstr#int$i', """
class A: public B {
public:
\tA(int i);

\t[{cursor_marker}]
};
""")

        self.verifySingleSnippet('class!A%public:B>private>constr#int$i<public>method#void@test#int$value', """
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

        self.verifySingleSnippet('class!A%public:B>private>constr#int$i<public>cmethod#void@test#int$value', """
class A: public B {
private:
\tA(int i){

\t}
public:
\tvoid test(int value) const{

\t}

\t[{cursor_marker}]
};
""")

        self.verifySingleSnippet('class!A%public:B>public>amethod#void@name', """
class A: public B {
public:
\tvirtual void name() = 0;

\t[{cursor_marker}]
};
""")

        self.verifySingleSnippet('class!A%public:B>public>acmethod#void@name', """
class A: public B {
public:
\tvirtual void name() const = 0;

\t[{cursor_marker}]
};
""")

        self.verifySingleSnippet('  class!A%public:B>public>amethod#void@name', """
  class A: public B {
  public:
  \tvirtual void name() = 0;

  \t[{cursor_marker}]
  };
""")

        self.verifySingleSnippet('  class!A%public:B>public>nimethod#void@name', """
  class A: public B {
  public:
  \tvoid name();

  \t[{cursor_marker}]
  };
""")

        self.verifySingleSnippet('  class!A%public:B>public>nicmethod#void@name', """
  class A: public B {
  public:
  \tvoid name() const;

  \t[{cursor_marker}]
  };
""")

        self.verifySingleSnippet('  class!A%public:B>private>nimethod#void@name', """
  class A: public B {
  private:
  \tvoid name();

  \t[{cursor_marker}]
  };
""")

        self.verifySingleSnippet('class!A%public:B>[[singleton]]', """
class A: public B {
public:
\tA& getInstance(){
\t\tstatic A instance;

\t\treturn instance;
\t}
private:
\tA(){}
\tA(A const& origin);
\tvoid operator=(A const& origin);

\t[{cursor_marker}]
};
""")

        self.verifySingleSnippet('class!Composite:Component%public>[[compositeclass]]public>method#void@traverse>[[compositemethod]]<', """
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

        self.verifySingleSnippet('class!A>public>dconstr#int$i', """
class A {
public:
\tA(int i) = delete;

\t[{cursor_marker}]
};
""")

        self.verifySingleSnippet('class!A>public>dmethod@nothing#void#int$i', """
class A {
public:
\tvoid nothing(int i) = delete;

\t[{cursor_marker}]
};
""")

        self.verifySingleSnippet('class!A>public>dcmethod@nothing#void#int$i', """
class A {
public:
\tvoid nothing(int i) const = delete;

\t[{cursor_marker}]
};
""")

        self.verifySingleSnippet('enum1!deca>pera&mika = 2&zika = 3', """
enum deca { pera, mika = 2, zika = 3, [{cursor_marker}] };
""")

        self.verifySingleSnippet('enum1!deca>pera&mika = 2&zika = 3<', """
enum deca { pera, mika = 2, zika = 3 };
[{cursor_marker}]
""")

        self.verifySingleSnippet('enum!deca>pera&mika = 2&zika = 3<', """
enum deca {
\tpera,
\tmika = 2,
\tzika = 3
};
[{cursor_marker}]
""")

    def testTemplate(self):
        self.verifySingleSnippet('class!A^T', """
template <class T>
class A {

};
[{cursor_marker}]
""")

        self.verifySingleSnippet('func#void@nothing^T', """
template <class T>
void nothing(){

}
[{cursor_marker}]
""")

        self.verifySingleSnippet('class!A>public>method#void@nothing^T', """
class A {
public:
\ttemplate <class T>
\tvoid nothing(){

\t}

\t[{cursor_marker}]
};
""")

    def testMethodImplementation(self):
        self.verifySingleSnippet('constri1!A#int$i', """
A::A(int i){

}
[{cursor_marker}]
""")

        self.verifySingleSnippet('methodi1!A#void@pera#int$i', """
void A::pera(int i){

}
[{cursor_marker}]
""")

        self.verifySingleSnippet('wblock!A>constri&constri$i$j#int&methodi#void@nothing', """
A::A(){

}

A::A(int i, int j){

}

void A::nothing(){

}

[{cursor_marker}]
""")

    def testNesting(self):
        self.verifySingleSnippet('if$one>if$two>if$3', """
if(one){
\tif(two){
\t\tif(3){

\t\t}
\t\t[{cursor_marker}]
\t}
}
""")

    def testMain(self):
        self.verifySingleSnippet('stdinc$stdio.h&[[main]]>printf("Hello, world\!");& &return 0;', """
#include <stdio.h>
int main(int argc, char* argv[]){
\tprintf("Hello, world!");

\treturn 0;
\t[{cursor_marker}]
}
""")