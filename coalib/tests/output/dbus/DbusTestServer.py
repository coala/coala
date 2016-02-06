import sys

try:
    import dbus
    import dbus.mainloop.glib
    from gi.repository import GLib

    from coalib.output.dbus.DbusServer import DbusServer
    skip, message = False, ''
except ImportError as err:
    skip, message = True, str(err)


def create_mainloop():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    # The BusName needs to be saved to a variable, if it is not saved - the
    # Bus will be closed.
    dbus_name = dbus.service.BusName("org.coala_analyzer.v1.test", session_bus)
    dbus_server = DbusServer(session_bus, "/org/coala_analyzer/v1/test",
                             on_disconnected=lambda: GLib.idle_add(sys.exit))
    mainloop = GLib.MainLoop()
    mainloop.run()


if __name__ == "__main__" and not skip:
    arg = ""
    if len(sys.argv) > 1:
        arg = sys.argv[1]

    if arg == "server":
        create_mainloop()
