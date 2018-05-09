.. _making_a_plugin:

===============
Making a plugin
===============

This page is intended as a guide for creating an editor plugin which uses homotopy to compile snippets.

Atom example_ can also be used as a reference.

Calling homotopy
----------------

Once installed with :code:`pip`, Homotopy can be used by calling :code:`homotopy` program.
It takes several arguments (see Arguments_ section) and prints the resulting snippet to stdout.
Warning messages are outputted to stderr.

On a high level, plugin should do the following:

* Collect arguments from editor.
* Call :code:`homotopy`.
* Replace snippet text with the result of :code:`homotopy` call.

Arguments
---------

There are several arguments that can be passed to :code:`homotopy`.

Only two are required, **language** and **snippet**,
but all of them should be provided by the plugin for full experience.

Language
""""""""

This is the first positional argument. It represents the name of the language the snippet should be compiled to.

Snippet
"""""""

This is the text of the snippet.

.. code-block:: bash

    homotopy c++ if$true

.. code-block:: text

    if(true){

    }


Cursor (-c)
"""""""""""

When flag :code:`-c` is present :code:`homotopy` will put text :code:`[{cursor_marker}]` at the place
where the cursor should be placed after the expansion of the snippet.

.. code-block:: bash

    homotopy -c c++ "if$true>"

.. code-block:: text

    if(true){
        [{cursor_marker}]
    }

Path (-p)
"""""""""

This optional argument that indicates the locations of custom snippets.
Value is *string* containing paths to snippet locations separated by :code:`::`.

.. code-block:: bash

    homotopy -p folder1::folder2 c++ if$true

.. code-block:: text

    if(true){

    }

Tab size (-t)
"""""""""""""

Homotopy uses tabs to indent code. If the editor is configured to use soft tabs (spaces instead of tabs),
use this option to indicate the size of one tab. All tabs in the result will be converted to the given number of spaces.

If this argument is not present, code with tabs will be returned.

.. code-block:: bash

    homotopy -t 4 c++ if$true

.. code-block:: text

    if(true){

    }

Cursor position
---------------

To make the user flow more natural,
homotopy can mark the location that the cursor should be in after the expansion of a snippet.

There are few things to keep in mind when implementing this feature.

* Look for :code:`[{cursor_marker}]` and replace it with cursor.
  Keep in mind that text *[{cursor_marker}]* should not be displayed.
* If, for any reason, :code:`[{cursor_marker}]` is not present,
  place the cursor in the line after the expanded snippet text.
* Make sure that the operation looks atomic with respect to undo/redo logic.

Settings
--------

Following user settings should be supported.

Homotopy location
"""""""""""""""""

If :code:`homotopy` is not in the user *PATH*, he/she should be able to configure the path to it.

User library
""""""""""""

Locations to user library folders should be configurable and passed to the engine with :code:`-p` argument.

Error handling
--------------

* If an error occurs (wrong path to :code:`homotopy` for example)
  when calling :code:`homotopy`, an error message should be displayed to the user.
* If any waring message is present (i.e. stderr is not empty),
  it should be displayed to the user (for example, so he/she can be informed when the snippet database is corrupt).





.. _example: https://github.com/Ahhhhmed/homotopy-atom