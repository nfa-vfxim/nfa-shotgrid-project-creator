"""Main start file for the NFA ShotGrid Project Creator, written by Mervin van Brakel (2024)"""

import sys

from PySide2 import QtWidgets

from controller import ProjectCreatorController

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    controller = ProjectCreatorController()

    sys.exit(app.exec_())
