import sys
from PyQt6.QtWidgets import QApplication
from src.gui.gui import AnalyzerUI


def main():
    app = QApplication(sys.argv)
    window = AnalyzerUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
