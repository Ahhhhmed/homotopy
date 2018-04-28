from test.stdlib_test import TestStdlib


class TestC(TestStdlib):
    def setUp(self):
        self.language = "C"

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
        self.verifySingleSnippet('struct!A>int a;', """
struct A {
\tint a;
\t[{cursor_marker}]
};
""")

        self.verifySingleSnippet('tdstruct!A>int a;&int b;', """
typedef struct{
\tint a;
\tint b;
\t[{cursor_marker}]
} A;
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
