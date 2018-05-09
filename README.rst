########
Homotopy
########

.. image:: https://travis-ci.org/Ahhhhmed/homotopy.svg?branch=master
    :target: https://travis-ci.org/Ahhhhmed/homotopy
.. image:: https://readthedocs.org/projects/homotopy/badge/?version=latest
    :target: http://homotopy.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://codecov.io/gh/Ahhhhmed/homotopy/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/Ahhhhmed/homotopy

Homotopy is a snippet compiler.
Instead of expanding and filling the blanks it lets you finish your thought and get the result you are expecting.

Write that complex thought in one line and let
Homotopy take care of parentheses, formatting, indent and all that boring stuff.

.. code-block:: text

    for#int$i%0%5>printf("Hello, five times.");

.. code-block:: C++

   for(int i=0; i<5; i++){
        printf("Hello, five times.");
   }

-------
Install
-------

.. code-block:: bash

    pip install homotopy

-------
Plugins
-------

This tool is intended to be used inside an editor. Currently only Atom plugin is implemented.

* `Atom`_

See `making a plugin`_ if you want to create a plugin.

---------------
Getting started
---------------

See `getting started`_ section in documentation.

.. _making a plugin: http://homotopy.readthedocs.io/en/latest/making_a_plugin.html
.. _getting started: http://homotopy.readthedocs.io/en/latest/getting_started.html
.. _Atom: https://atom.io/packages/homotopy