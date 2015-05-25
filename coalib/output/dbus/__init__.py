"""
This package holds dbus related objects. Dbus objects are used to communicate
between coala and other applications using dbus.

All dbus clients will first connect to the DbusServer, and request the
DbusServer to create documents which can be analyzed. The DbusServer internally
handles different clients separately so that it is possible for multiple
clients to connect simultaneously.
Once the client creates a document, the object path of the document is returned
and the client can use it to analyze the document (which happens in the
DbusDocument.
"""
