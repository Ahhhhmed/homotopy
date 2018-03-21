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

Utilities
^^^^^^^^^

Utility functionality to help the development of editor add-ons.

Application frontend
^^^^^^^^^^^^^^^^^^^^

Console application frontend.

.. links
.. _Ply: http://www.dabeaz.com/ply/