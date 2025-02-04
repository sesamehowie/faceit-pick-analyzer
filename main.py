import os
import sys
import ctypes
from PyQt6.QtWidgets import QApplication

os.environ["QT_SCALE_FACTOR_ROUNDING_POLICY"] = "PassThrough"

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    pass


def main():
    app = QApplication(sys.argv)

    from src.gui.gui import AnalyzerUI

    window = AnalyzerUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
