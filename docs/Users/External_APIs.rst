External APIs
=============

Use *coala* to make your application better.

DBus
----

The *coala* DBus API essentially creates a server which can have multiple
clients connected to it. The clients communicate to the *coala* server
using DBus. To start the server, first install *coala* and then simple run
``coala-dbus``.

This spawns a bus with the name ``org.coala_analyzer.v1`` as a
SessionBus and can be verified and tested using a DBus debugger like
`DFeet <https://wiki.gnome.org/Apps/DFeet>`__. The bus has 1 object-path
by default - ``/org/coala_analyzer/v1``. This is the first point of
contact with *coala* for any client.

The object-path ``/org/coala_analyzer/v1`` has the interface
``org.coala_analyzer.v1`` which contains the two methods -
``CreateDocument`` and ``DisposeDocument``. These are used to tell *coala*
about the documents you wish to analyze.

``CreateDocument``
~~~~~~~~~~~~~~~~~~

**Args**: the path of the document

**Returns**: object-path for the document

A document is defined by it's path. The path should be a absolute path,
not a relative one. This method returns an object-path which will be
hence forth used to interact with that document.

``DisposeDocument``
~~~~~~~~~~~~~~~~~~~

**Args**: the path to the document

**Returns**: none

It disposes the object-path corresponding to the given path.

Now, the object-path returned by the ``CreateDocument`` method also has
the interface ``org.coala_analyzer.v1``. This interface is used to
handle which config file *coala* will use to analyze the document, and the
function to get analysis results. It contains 4 functions:

``GetConfigFile``
~~~~~~~~~~~~~~~~~

**Args**: none

**Returns**: the config file path

``SetConfigFile``
~~~~~~~~~~~~~~~~~

**Args**: the config file path

**Returns**: the config path which is set after it executes.

``FindConfigFile``
~~~~~~~~~~~~~~~~~~

**Args**: the config file path

**Returns**: the config path which is set after it executes.

It attempts to find the config file related to the file by searching in
parent directories till it finds a ``.coafile``.

``Analyze``
~~~~~~~~~~~

**Args**: none

**Returns**: an array of DBus structures containing:

* The name of the section
* Boolean which is true if all bears in the section executed successfully
* List of results where each result is a list which contains:
  (str)origin, (str)message, (str)file, (str)line\_nr, (str)severity
