#!/usr/bin/env python3

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License
# for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys

import dbus
import dbus.mainloop.glib
from coalib.misc import Constants
from coalib.output.dbus.DbusServer import DbusServer
from gi.repository import GLib


def sys_clean_exit():
    sys.exit(0)


def on_disconnected():
    return GLib.idle_add(sys_clean_exit)


def main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    # The BusName needs to be saved to a variable, if it is not saved - the
    # Bus will be closed.
    dbus_name = dbus.service.BusName(  # pylint: disable=unused-variable
        Constants.BUS_NAME,
        session_bus)
    DbusServer(session_bus,
               '/org/coala_analyzer/v1',
               on_disconnected=on_disconnected)

    mainloop = GLib.MainLoop()
    mainloop.run()


if __name__ == '__main__':  # pragma: no cover
    main()
