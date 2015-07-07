from subprocess import call
import sys
import os

from coalib.output.gui.coalaApp import coalaApp


def main():
    data_path = os.path.join(os.path.dirname(__file__),
                             "output",
                             "gui",
                             "data")
    if not os.path.exists(os.path.join(data_path, "coala.gresource")):
        print("Calling ",
              "glib-compile-resources",
              os.path.join(data_path, "coala.gresource.xml"),
              "--sourcedir="+data_path)
        call(["glib-compile-resources",
              os.path.join(data_path, "coala.gresource.xml"),
              "--sourcedir="+data_path])


    app = coalaApp()
    app.run(sys.argv)
