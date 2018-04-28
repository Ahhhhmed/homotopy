===============
Getting started
===============

Homotopy is a snippet language. It is designed with the focus on writing code and not caring about how it looks.
That is handled automatically.

This document designed to get you up and running with using Homotopy. It uses *C++* as a working language.

-----------
Hello world
-----------

.. code-block:: text

    stdinc$stdio.h& &[[main]]>printf("Hello, world\!");&return 0;

.. code-block:: C

    #include <stdio.h>

    int main(int argc, char* argv[]){
        printf("Hello, world!");

        return 0;
    }

That was a lot of code for one line.
Following sections wil gradually introduce concepts used in the *"Hello, World!"* example.

--------
Language
--------

Snippet definitions
^^^^^^^^^^^^^^^^^^^

Snippet is defined as text with placeholders for parameter values.

.. code-block:: json

    {"name": "stdinc","language": "C++","snippet": "#include <$$$>"}

This is the definition for *C++* snippet for including from standard library.
:code:`$$$` is a placeholder for parameter :code:`$`.

Example:

.. code-block:: text

    stdinc$stdio.h

.. code-block:: C

    #include <stdio.h>

Parameters
^^^^^^^^^^

Parameters are used to bind values to a snippet definition. Parameters begin with on of the following characters.

*NOTE: This is just a convention that standard library follows. It is not enforced by any part of the tool.
Have that in mind if creating custom snippets.*

============== ===========
Parameter name Description
============== ===========
!              Class name
~              Implements
:              Extends
^              Template
@              Method/function name
#              Type
$              Value
%              Other
============== ===========

.. code-block:: text

    func#void@foo

.. code-block:: C

    void foo(){

    }

Parameters can be used more than once in the same snippet.

.. code-block:: text

    func#void@foo#int$i#int$j

.. code-block:: C

    void foo(int i, int j){

    }

In the last example there are two adjacent int parameters of foo.
Passing two value parameters first and then a single type parameter gives the same result.

.. code-block:: text

    func#void@foo$i$j#int

.. code-block:: C

    void foo(int i, int j){

    }

Into
^^^^

There is another, special, parameter, into :code:`>`. It separates a parent and child snippets.
Child snippet is substituted inside parent snippet at the placeholder :code:`>>>` position.

.. code-block:: text

    if$i==4>printf("four");

.. code-block:: C

    if(i==4){
        printf("four");
    }

In this way, several snippets can be combined to make up a larger construct.

Following control characters are used to combine snippets.

============== ===========
Parameter name Description
============== ===========
>              Into
<              Out
&              And
============== ===========

Example with :code:`<`:

.. code-block:: text

    if$i==4>printf("four");<printf("out of if");

.. code-block:: C

    if(i==4){
        printf("four");
    }

    printf("out of if");

Example with :code:`&`:

.. code-block:: text

    printf("first line");&printf("second line");

.. code-block:: C

    printf("first line");

    printf("second line");

Escape
^^^^^^

Control character are picked so they don't interfere with code too much. Yet sometimes code contains control characters.
To make any character part of snippet and not treat it as a parameter just put backslash character :code:`'\'` in front of that character.

Example:

.. code-block:: text

    if$a \> max>max = a

.. code-block:: C

    if(a > max){
        max = a
    }

Shortcuts
^^^^^^^^^

There are common construction that are tedious to write. To help with that, Homotopy has a concept of shortcuts.

Anywhere in the snippet, place a definition inside double square brackets and it gets expanded before compilation.

Example:

.. code-block:: text

    [[main]]

.. code-block:: C

    int main(int argc, char* argv[]){

    }

---------------------
Hello world deep dive
---------------------

Lets take a look at the hello world snippet once again and go through the process of compilation in detail.
This is a fairly large example but includes most of the feathers of Homotopy.

.. code-block:: text

    stdinc$stdio.h&[[main]]>printf("Hello, world\!");&return 0;

At the top level there are three snippets:

1. :code:`stdinc$stdio.h` and
2. Space for an empty line.
3. :code:`[[main]]>printf("Hello, world\!");&return 0;`

They are implicitly inside an implicit :code:`block` snippet. Block snippet just separate snippets lines.

Definitions used to compile this snippet:

.. code-block:: json

    [
    {"name": "stdinc","language": "C++","snippet": "#include <$$$>"},
    {"name": "main","language": "C++","snippet": "func#int@main#int$argc#char*$argv[]"},
    {"name": "func","language": "C++","snippet": "### @@@({{params}}){\n{{inside_wblock}}\n}"},
    {"name": "params","language": "C++","snippet": "### $$${{opt_params}}"},
    {"name": "opt_params","language": "C++","snippet": ", ### $$${{opt_params}}"},
    {"name": "inside_wblock","language": "C++","snippet": "\t>>>{{opt_inside_wblock}}"},
    {"name": "opt_inside_wblock","language": "C++","snippet": "\n\n\t>>>{{opt_inside_wblock}}"}
    ]

:code:`stdinc` has the definition :code:`#include <$$$>`
and :code:`stdio.h` just gets replaced in to get :code:`#include <stdio.h>`

Lets now go through the third snippet step by step:

1. :code:`[[main]]` gets expanded into :code:`func#int@main#int$argc#char*$argv[]`.
2. :code:`func` get expanded into :code:`### @@@({{params}}){\n{{inside_wblock}}\n}`.
3. :code:`###` gets replaced with :code:`int`.
4. :code:`@@@` gets replaced with :code:`main`.
   Now, partial result is :code:`int main({{params}}){\n{{inside_wblock}}\n}`.
5. :code:`###` is not present in the current partial result so :code:`{{params}}` gets expanded
   because it contains :code:`###`.
   New partial result is :code:`int main(### $$${{opt_params}}){\n{{inside_wblock}}\n}`.
6. :code:`###` gets replaced with :code:`int`.
7. :code:`$$$` gets replaced with :code:`argc`.
8. Similar to **5**, :code:`{{opt_params}}` gets replaced with :code:`, ### $$${{opt_params}}`.
9. :code:`###` gets replaced with :code:`char*`.
10. :code:`$$$` gets replaced with :code:`argv[]`.
11. Similar to **5** and **8**, :code:`{{inside_wblock}}` gets replaced with :code:`\t>>>{{opt_inside_wblock}}`.
12. Compile snippet :code:`printf("Hello, world\!");`.
    This is trivial in this case and the result :code:`printf("Hello, world!");`.
    :code:`!` gets escaped and everything else stays the same.
13. :code:`>>>` gets replaced with :code:`printf("Hello, world!");`.
14. Similar to **5**, **8** and **11**, :code:`{{opt_inside_wblock}}` gets replaced with :code:`\n\n\t>>>{{opt_inside_wblock}}`.
15. :code:`return 0;` get trivially compiled to :code:`return 0;`.
16. :code:`>>>` gets replaced with :code:`return 0;`.
17. Result gets cleaned from sub-snippets like :code:`{{opt_inside_wblock}}` and :code:`{{opt_params}}`.

.. code-block:: C

    #include <stdio.h>

    int main(int argc, char* argv[]){
        printf("Hello, world!");

        return 0;
    }
