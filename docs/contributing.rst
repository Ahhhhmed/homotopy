============
Contributing
============

-------------------
Development process
-------------------

Code changes should be made in the following way:

* Create a new branch.
* Add code and unit tests. All code should be covered with tests.
* Run tests locally.
* Make a pull request and make sure that travis build succeeds.

----------
Local copy
----------

Getting local copy:

.. code-block:: bash

   $git clone https://github.com/Ahhhhmed/homotopy.git

Running tests (run from the project root):

.. code-block:: bash

   $python -m unittest

---------
Internals
---------

The code is separated in several components:

* `Preprocessor`_
* `Parser`_
* `Syntax tree`_
* `Snippet provider`_
* `Compiler`_
* `Application frontend`_

Preprocessor
^^^^^^^^^^^^

Before parsing and creating syntax tree some prepossessing is done to enable some feathers.
They are described in following sections.

Decorators
""""""""""

Consider following example:

.. code-block:: text

   1. for#int$i%n
   2. for[[sup]]

And following snippet definition:

.. code-block:: json

    {"name": "sup","language": "C++","snippet": "#int$i%n"}

This pattern occurs often and it is useful to name it and use it by name ('sub' stands for 'standard up').
More realistic examples are design pattern implementation (singleton for example).
Another advantage of this approach is that multiple decorators can be combined to make a more complex construction.

Preprocessor detects decorators that are defined in double square brackets and expands them using snippet provider.

Cursor marker
"""""""""""""

After expanding a snippet user should have the cursor at a convenient location.
The following rule is followed.


*Writing some text after expanding the snippet should have the same effect as
writing that text and expanding the snippet afterwords.*


To enable this preprocessor appends :code:`&[{cursor_marker}]` to the snippet text
so a plugin can put cursor at the marker location.

Usage
"""""

.. autoclass:: homotopy.preprocessor.Preprocessor
    :members: expand_decorators, put_cursor_marker
    :member-order: bysource

.. code-block:: python

    from homotopy.preprocessor import Preprocessor
    from homotopy.snippet_provider import SnippetProvider

    preprocessor = Preprocessor(SnippetProvider('python', ['folder1', 'folder2']))
    snippet = "for"
    expanded_snippet = preprocessor.expand_decorators(snippet)
    expanded_snippet_with_cursor = preprocessor.put_cursor_marker(expanded_snippet)

Parser
^^^^^^

Responsible for converting snippet string to a syntax tree instance.

Parameters
""""""""""

Basic functionality is adding parameters to a snippet.

.. code-block:: text

   snippet#parameter1$parameter2

This should become:

.. code-block:: text

               $
              / \
             /   \
            #    parameter2
           / \
          /   \
     snippet  parameter1

Following characters are used to indicate parameters:

.. code-block:: python

    {'!', '@', '#', '$', '%', ':', '~'}

Inside snippets
"""""""""""""""

Snippets can have other snippets insight them (like body of a for loop for example).
Snippets are separated by special characters that determine their relations.

* :code:`>` move to the inside of a snippet
* :code:`<` move to another snippet on the level above
* :code:`&` move to another snippet on the same level

Example:

.. code-block:: text

    for>if>if<if&if

This should be translated to:

.. code-block:: text

                       >
                      / \
                     /   \
                    >    if
                   / \
                  /   \
                 >    if
                / \
               /   \
              for   >
                   / \
                  /   \
                 if   if

Character :code:`>` is used to donate the inside of a snippet in snippet definitions.
This is why all occurrences of :code:`<` and :code:`&` are translated to :code:`>`.

Implicit snippet
""""""""""""""""

Consider following example:

.. code-block:: text

    for>if<while

The :code:`while` is not a part of :code:`for` snippet.
Parser creates an implicit :code:`block` snippet at the beginning.
:code:`block` snippet is implemented as a list of sub-snippets in new lines.

Escape sequence
"""""""""""""""

Homotopy uses escape sequence to enable operator usage in snippets.
Character after :code:`'\'` will always be a part of snippet and not recognised as an operator.

Usage
"""""

.. autoclass:: homotopy.parser.Parser
    :members: parse
    :member-order: bysource

.. code-block:: python

    from homotopy.parser import Parser

    parser = Parser()
    snippet = "for"
    syntax_tree = parser.parse(snippet)

Syntax tree
^^^^^^^^^^^

Tree structure of a snippet.

.. automodule:: homotopy.syntax_tree
    :members:

Usage
"""""

.. code-block:: python

    from homotopy.syntax_tree import SimpleSnippet, CompositeSnippet

    simple_snippet = SimpleSnippet("for")
    composite_snippet = CompositeSnippet(simple_snippet, '>', SimpleSnippet('code'))

Snippet provider
^^^^^^^^^^^^^^^^

Provides snippets definitions from a database of snippets.

Snippet definition files
""""""""""""""""""""""""

Snippets definition are writen in json files as shown is the following example.

.. code-block:: json

    [
    {"name": "for","language": "C++","snippet": "for(###){$$$}"},
    {"name": "if","language": ["C++", "java"],"snippet": "if(###){$$$}"}
    ]

Note that language can be a string or a list of strings. Use :code:`all` for snippets that should always be included.
Language can be excluded by prefixing it with :code:`~` (for example :code:`~c++`).

Snippet provider reads all the files containing snippets.
It searches all json files contained in the given list of folders files.
The list of folders is specified in the :code:`path` variable (similar to :code:`os.path`).

Usage
"""""

.. autoclass:: homotopy.snippet_provider.SnippetProvider
    :members: __getitem__, __init__
    :member-order: bysource

.. code-block:: python

    from homotopy.snippet_provider import SnippetProvider

    provider = SnippetProvider("C++", ["folder1", "folder2"])
    snippet = "for"
    snippetExpansion = provider[snippet]

Compiler
^^^^^^^^

Compiler is responsible for turning a syntax tree into output code. It uses `snippet provider`_ for simple snippets.
General rules used by compiler will be discussed in this section.

Simple substitution
"""""""""""""""""""

Consider the following snippet definition.

.. code-block:: json

    {"name": "if","language": "C++","snippet": "if(###){$$$}"}

Snippet :code:`if#true$i=3;` is expanded in the following way:

* :code:`if` becomes :code:`if(###){$$$}` from the definition.
* :code:`###` gets replaced by :code:`true` to get :code:`if(true){$$$}`.
* :code:`$$$` gets replaced by :code:`i=3;` to get the final output :code:`if(true){i=3;}`.

The value of an operator gets replace by the value provided in the snippet.
This is done for every operator to get the final result.
Note that there are 3 characters in snippet definition and only one in the snippet.
The reason for this is that special characters used by homotopy are also used by other programming languages.
For example, :code:`$` is a part of a variable name in php.

Definition expansion
""""""""""""""""""""

Consider a snippet for a function call. Writing :code:`fun!foo#a#b#c` should return :code:`foo(a,b,c)`.
To write a single snippet definition for all functions would mean supporting variable number of parameters.

This is possible using snippet definitions inside snippets.

.. code-block:: json

    [
    {"name": "fun","language": "python","snippet": "!!!({{params}})"},
    {"name": "params","language": "python","snippet": "###{{opt_params}}"},
    {"name": "opt_params","language": "python","snippet": ", ###{{opt_params}}"}
    ]

Snippet :code:`fun!foo#a#b` is expanded in the following way:

* :code:`fun` becomes :code:`!!!({{params}})` from the definition.
* :code:`!!!` gets replaced by :code:`foo` to get :code:`foo({{params}})`.
* :code:`###` does not exist in :code:`foo({{params}})` so :code:`{{params}}` get expanded to :code:`###{{opt_params}}`.
* :code:`###` gets replaced by :code:`a;` to get :code:`foo(a{{opt_params}})`
* :code:`###` does not exist in :code:`foo(a{{opt_params}})` so :code:`{{opt_params}}`
  get expanded to :code:`, ###{{opt_params}}`.
* :code:`###` gets replaced by :code:`b;` to get :code:`foo(a, b{{opt_params}})`.
* :code:`{{opt_params}}` gets removed from final result to get :code:`foo(a,b)`.

Expansion is done in case `simple substitution`_ can't be done.
This enables recursive constructs as shown in the example above.

Note that there might be multiple sub-snippets inside a single snippet.
In that case the first one containing required operator in its definition gets expanded.
Other sub-snippets do not get expanded.

Outer parameters
""""""""""""""""

Accessing outer parameters can be done in the following way:

.. code-block:: json

    [
    {"name": "constructor","language": "java","snippet": "public {{?###}}(){}"}
    ]

The snippet above would create a public empty constructor. :code:`{{?###}}` binds to the same value as :code:`{{?###}}`
from the snippet above the current one.

Usage
"""""

.. autoclass:: homotopy.compiler.Compiler
    :members: compile
    :member-order: bysource

.. code-block:: python

    from homotopy.compiler import Compiler
    from homotopy.parser import Parser
    from homotopy.snippet_provider import SnippetProvider
    from homotopy.util import IndentManager

    snippet_provider = SnippetProvider('python', ['folder1', 'folder2'])
    indent_manager = IndentManager(snippet_provider)

    compiler = Compiler(snippet_provider, indent_manager)
    parser = Parser()

    snippet = "for>code"
    syntax_tree = parser.parse(snippet)

    compiled_snippet = compiler.compile(syntax_tree)

Application frontend
^^^^^^^^^^^^^^^^^^^^

Homotopy class
""""""""""""""

:code:`Homotopy` class scarves as a facade for the whole tool. It should be the eatery point for snippet compilation.
It can be configured to include additional paths to user defined snippet libraries.

Example:

.. code-block:: python

    from homotopy import Homotopy

    cpp_snippets = Homotopy("c++")
    print(cpp_snippets.compile('int n=5;&for#int$i%n>printf("hello");'))

outputs:

.. code-block:: text

    int n=5;
    for(int i=0; i<n; i++){
        printf("hello");
    }

.. autoclass:: homotopy.Homotopy
    :members: compile, add_lib_folder

Console application
"""""""""""""""""""

Homotopy can also be used as a console application. In fact, this is the intended way of using is via editor plugins.

.. code-block:: text

    C:\dev\homotopy>homotopy -h
    usage: homotopy [-h] [-t N] [-c] [-p PATH] language snippet

    Compile a snippet.

    positional arguments:
      language              Language for the snippet to be compiled to
      snippet               A snippet to be compiled

    optional arguments:
      -h, --help            show this help message and exit
      -t N, --tabsize N     Number of spaces in one tab. Tabs remain tabs if
                            absent
      -c, --cursor          Indicate cursor marker in compiled snippet
      -p PATH, --path PATH  Path to snippet library folders separated by :


