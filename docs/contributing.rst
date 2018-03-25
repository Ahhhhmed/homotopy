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
* `Utilities`_
* `Application frontend`_

Parser
^^^^^^

Responsible for converting snippet string to a syntax tree instance. Uses Ply_ to do the parsing.

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

Utilities
^^^^^^^^^

Utility functionality to help the development of editor add-ons.

Application frontend
^^^^^^^^^^^^^^^^^^^^

Console application frontend.

.. links
.. _Ply: http://www.dabeaz.com/ply/