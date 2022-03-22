from PySide2 import QtWidgets
from MainWindow import MainWindow

if __name__ == "__main__":
    import sys
    a = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(a.exec_())
