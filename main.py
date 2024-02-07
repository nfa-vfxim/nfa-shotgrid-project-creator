"""Main start file for the NFA ShotGrid Project Creator, written by Mervin van Brakel (2024)"""

import sys

from PySide2 import QtWidgets

from view import ProjectCreatorView

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = ProjectCreatorView()
    widget.show()

    sys.exit(app.exec_())
