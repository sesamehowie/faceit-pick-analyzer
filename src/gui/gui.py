import asyncio
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QHeaderView,
)
from PyQt6.QtGui import QColor
from src.gui.styles import dark_stylesheet
from runner import Runner
from data.config import API_KEY


class AnalyzerUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FACEIT Analyzer")
        self.setGeometry(200, 200, 800, 600)
        self.setStyleSheet(dark_stylesheet)

        layout = QVBoxLayout()

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Paste your URL here...")
        layout.addWidget(self.url_input)

        self.run_button = QPushButton("Start Analysis", self)
        self.run_button.clicked.connect(self.run_script)
        layout.addWidget(self.run_button)

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(2)
        self.result_table.setHorizontalHeaderLabels(["Key", "Value"])

        self.result_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.result_table)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    async def fetch_data(self, match_id):
        """Fetch data using Runner (replace with actual API call if needed)"""
        runner = Runner(api_key=API_KEY, match_id=match_id)
        data = [("Map", "Win Probability")]
        res = await runner.run()
        data.extend(res)
        return data

    async def run_script_async(self):
        """Run script asynchronously and update UI"""
        url = self.url_input.text().strip()
        if not url:
            self.status_label.setText("❌ Please enter a valid URL!")
            return

        try:
            match_id = url.split("/")[6]
        except IndexError:
            self.status_label.setText("❌ URL format is incorrect!")
            return

        self.status_label.setText(f"Fetching data for Match ID: {match_id}")

        data = await self.fetch_data(match_id)

        self.result_table.setRowCount(len(data))
        for row, (key, value) in enumerate(data):
            key_item = QTableWidgetItem(key)
            value_item = QTableWidgetItem(value)

            key_item.setBackground(QColor("#1E1E1E"))
            key_item.setForeground(QColor("#FFFFFF"))
            value_item.setBackground(QColor("#1E1E1E"))
            value_item.setForeground(QColor("#FFFFFF"))

            self.result_table.setItem(row, 0, key_item)
            self.result_table.setItem(row, 1, value_item)

        self.status_label.setText("✅ Processing complete!")

    def run_script(self):
        """Wrapper to run async function in PyQt"""
        asyncio.run(self.run_script_async())
