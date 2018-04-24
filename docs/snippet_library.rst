===============
Snippet library
===============

This document contains snippet examples for most of snippets from standard library.

----
Core
----

There are few snippets that are used to create the structure of snippets.
They can also be used to add parameters that can be used inside the snippet.

block:

.. code-block:: text

    block>line1&line2

.. code-block:: C

    line1
    line2

-----------------

wblock (wide block):

.. code-block:: text

    wblock>line1&line2

.. code-block:: C

    line1

    line2

*Note that* :code:`wblock` *is the implicit parent of all snippets. Next snippet sill have the same result.*

.. code-block:: text

    line1&line2

.. code-block:: C

    line1

    line2

---
C++
---

Commands
^^^^^^^^

stdinc:

.. code-block:: text

    stdinc$stdio.h

.. code-block:: C

    #include <stdio.h>

---------------------------

inc:

.. code-block:: text

    inc$homotopy.h

.. code-block:: C

    #include "homotopy.h"

Flow control
^^^^^^^^^^^^

for:

.. code-block:: text

    for#int$i%0%n

.. code-block:: C

    for(int i=0; i<n; i++){

    }

---------------------------

forr:

.. code-block:: text

    forr#int$i%n%0

.. code-block:: C

    for(int i=n; i>=0; i--){

    }

---------------------------

forin:

.. code-block:: text

    forin#int$i%array

.. code-block:: C

   for(int i: array){

   }

---------------------------

if:

.. code-block:: text

    if$true>printf("Always");

.. code-block:: C

   if(true){
       printf("Always");
   }

---------------------------

while:

.. code-block:: text

    while$true>printf("Forever and always");

.. code-block:: C

   while(true){
       printf("Forever and always");
   }

---------------------------

switch:

.. code-block:: text

    switch$i>case$1>printf("one");<case$2>printf("two");

.. code-block:: C

   switch(i){
       case 1:
           printf("one");
           break;

       case 2:
           printf("two");
           break;
   }

---------------------------

.. code-block:: text

    switch$i>case$1$2>printf("one or two");

.. code-block:: C

   switch(i){
       case 1:
       case 2:
           printf("one or two");
           break;
   }

---------------------------

Objects
^^^^^^^

struct:

.. code-block:: text

    struct!pair>int first, second;

.. code-block:: C++

   struct pair {
       int first, second;
   };

---------------------------

class:

.. code-block:: text

    class!A:B%public>private>int a;<public>int b;

.. code-block:: C++

   class A: public B {
   private:
       int a;
   public:
       int b;
   };

---------------------------

enum:

.. code-block:: text

    enum!Colors>red&green&blue

.. code-block:: C++

   enum Colors {
       red,
       green,
       blue
   };

---------------------------

enum1 (enum in single line):

.. code-block:: text

    enum1!Colors>red&green&blue

.. code-block:: C++

   enum Colors { red, green, blue };

Functions
^^^^^^^^^

func (function):

.. code-block:: text

    func#int@five>return 5;

.. code-block:: C++

   int five(){
       return 5;
   }

---------------------------

.. code-block:: text

    func#int@plus#int$i#int$j>return i+j;

.. code-block:: C++

   int plus(int i, int j){
       return i+j;
   }

---------------------------

.. code-block:: text

    func#int@plus$i$j#int>return i+j;

.. code-block:: C++

   int plus(int i, int j){
       return i+j;
   }

*Note that values* :code:`i` *and* :code:`j` *are specified first and type int after.
This makes both* :code:`i` *and* :code:`j` *ints without typing int twice.*

---------------------------

method:

.. code-block:: text

    class!A>public>method#int@five>return 5;

.. code-block:: C++

   class A {
   public:
       int five(){
           return 5;
       }
   };

---------------------------

nimethod (not implemented method):

.. code-block:: text

    class!A>public>nimethod#int@five

.. code-block:: C++

   class A {
   public:
       int five();
   };

---------------------------

amethod (abstract method):

.. code-block:: text

    class!A>public>amethod#int@five

.. code-block:: C++

   class A {
   public:
       int five() = 0;
   };

---------------------------

dmethod (deleted method):

.. code-block:: text

    class!A>public>dmethod#int@five

.. code-block:: C++

   class A {
   public:
       int five() = delete;
   };

---------------------------

methodi1 (single method implementation):

.. code-block:: text

    methodi1!A#int@five>return 5;

.. code-block:: C++

   int A::five(){
       return 5;
   }

---------------------------

mithodi (method implementation):

.. code-block:: text

    wblock!A>methodi#int@five>return 5;<methodi#int@six>return 6;

.. code-block:: C++

   int A::five(){
       return 5;
   }

   int A::six(){
       return 6;
   }

*Note that* :code:`wblock` *is used here to bind class parameter that is used by both children snippets.*

---------------------------

constr (constructor):

.. code-block:: text

    class!A>public>constr#int$i

.. code-block:: C++

   class A {
   public:
       A(int i){

       }
   };

Templates
^^^^^^^^^

template:

.. code-block:: text

    template^T>class!A

.. code-block:: C++

   template <class T>
   class A {

   };

---------------------------

.. code-block:: text

    template^T>func@nothing#void

.. code-block:: C++

   template <class T>
   void nothing(){

   }

Design Patterns
^^^^^^^^^^^^^^^

singleton:

.. code-block:: text

    class!A>[[singleton]]

.. code-block:: C++

   class A {
   public:
       A& getInstance(){
           static A instance;

           return instance
       }
   private:
       A(){}
       A(A const& origin);
       void operator=(A const& origin);
   };

---------------------------

composite (class and method):

.. code-block:: text

    class!Composite:Component%public>[[compositeclass]]&public>method#void@traverse[[compositemethod]]

.. code-block:: C++

   class Composite: public Component {
   public:
       void add(Component *item){
           children.puch_back(item);
       }
   private:
       std::vector<Component*> children;
   public:
       void traverse(){
           for(int i=0; i<children.size(); i++){
               children[i]->traverse();
           }
       }
   };