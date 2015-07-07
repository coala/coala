import sys
from coalib.output.gui.coalaApp import coalaApp


def main():
    app = coalaApp()
    app.run(sys.argv)
