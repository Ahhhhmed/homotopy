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

* `Parser`_
* `Syntax tree`_
* `Snippet provider`_
* `Compiler`_
* `Utilities`_
* `Application frontend`_

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


Syntax tree
^^^^^^^^^^^

Tree structure of a snippet.

.. automodule:: homotopy.syntax_tree
    :members:

Snippet provider
^^^^^^^^^^^^^^^^

Provides snippets definitions from a database of snippets.

Snippet definition files
""""""""""""""""""""""""

Snippets definition are writen in json files as shown is the following example.

.. code-block:: json

    [
    {"name": "for","language": "C++","snippet": "for(#){$}"},
    {"name": "if","language": "C++","snippet": "if(#){$}"}
    ]

Implementation
""""""""""""""

Snippet provider reads all the files containing snippets.
It searches all json files contained in the given list of folders files.
The list of folders is specified in the :code:`path` variable (similar to :code:`os.path`).

.. autoclass:: homotopy.snippet_provider.SnippetProvider
    :members: __getitem__, __init__
    :member-order: bysource

Usage
"""""

Using this class should be straightforward. Look.

.. code-block:: python

    provider = SnippetProvider("C++", ["folder1", "folder2"])
    snippet = "for"
    snippetExpansion = provider[snippet] # snippetExpansion == "for(#){$}" if used json from above

Compiler
^^^^^^^^

Compiler is responsible for turning a syntax tree into output code. It uses `snippet provider`_ for simple snippets.
General rules used by compiler will be discussed in this section.

Simple substitution
"""""""""""""""""""

Consider the following snippet definition.

.. code-block:: json

    {"name": "if","language": "C++","snippet": "if(#){$}"}

Snippet :code:`if#true$i=3;` is expanded in the following way:

* :code:`if` becomes :code:`if(#){$}` from the definition.
* :code:`#` gets replaced by :code:`true` to get :code:`if(true){$}`.
* :code:`$` gets replaced by :code:`i=3;` to get the final output :code:`if(true){i=3;}`.

The value of an operator gets replace by the value provided in the snippet.
This is done for every operator to get the final result.

Definition expansion
""""""""""""""""""""

Consider a snippet for a function call. Writing :code:`fun!foo#a#b#c` should return :code:`foo(a,b,c)`.
To write a single snippet definition for all functions would mean supporting variable number of parameters.

This is possible using snippet definitions inside snippets.

.. code-block:: json

    [
    {"name": "fun","language": "python","snippet": "!({{params}})"},
    {"name": "params","language": "python","snippet": "#{{opt_params}}"},
    {"name": "opt_params","language": "python","snippet": ", #{{opt_params}}"}
    ]

Snippet :code:`fun!foo#a#b` is expanded in the following way:

* :code:`fun` becomes :code:`!({{params}})` from the definition.
* :code:`!` gets replaced by :code:`foo` to get :code:`foo({{params}})`.
* :code:`#` does not exist in :code:`foo({{params}})` so :code:`{{params}}` get expanded to :code:`#{{opt_params}}`.
* :code:`#` gets replaced by :code:`a;` to get :code:`foo(a{{opt_params}})`
* :code:`#` does not exist in :code:`foo(a{{opt_params}})` so :code:`{{opt_params}}`
  get expanded to :code:`, #{{opt_params}}`.
* :code:`#` gets replaced by :code:`b;` to get :code:`foo(a, b{{opt_params}})`.
* :code:`{{opt_params}}` gets removed from final result to get :code:`foo(a,b)`.

Expansion is done in case `simple substitution`_ can't be done.
This enables recursive constructs as shown in the example above.
Number of expansion performed is capped to prevent infinite recursions.

Utilities
^^^^^^^^^

Utility functionality to help the development of editor add-ons.

Application frontend
^^^^^^^^^^^^^^^^^^^^

Console application frontend.
