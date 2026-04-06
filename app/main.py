import sys
import os
import subprocess
from unittest import result
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox
)
from PyQt6.QtCore import Qt


class SimulationApp(QMainWindow):
    """Main window for the TwoConnectedTanks simulation launcher."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenModelica Simulation Launcher")
        self.setMinimumWidth(500)
        self.setup_ui()

    def setup_ui(self):
        """Set up all UI components."""

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Input Field 1: Application path
        app_label = QLabel("Simulation Executable:")
        self.app_path_input = QLineEdit()
        self.app_path_input.setPlaceholderText("Select the TwoConnectedTanks executable...")
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_executable)

        app_row = QHBoxLayout()
        app_row.addWidget(self.app_path_input)
        app_row.addWidget(browse_button)

        # Input Field 2: Start Time
        start_label = QLabel("Start Time (integer, >= 0):")
        self.start_time_input = QLineEdit()
        self.start_time_input.setPlaceholderText("e.g. 0")

        # Input Field 3: Stop Time
        stop_label = QLabel("Stop Time (integer, < 5):")
        self.stop_time_input = QLineEdit()
        self.stop_time_input.setPlaceholderText("e.g. 3")

        # Run Button
        self.run_button = QPushButton("Run Simulation")
        self.run_button.setFixedHeight(40)
        self.run_button.clicked.connect(self.run_simulation)

        # added everything to main layout
        main_layout.addWidget(app_label)
        main_layout.addLayout(app_row)
        main_layout.addWidget(start_label)
        main_layout.addWidget(self.start_time_input)
        main_layout.addWidget(stop_label)
        main_layout.addWidget(self.stop_time_input)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.run_button)


    def browse_executable(self):
        """Open file dialog to select the simulation executable."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Simulation Executable",
            "",
            "Executable Files (*.exe)"
        )
        if file_path:
            self.app_path_input.setText(file_path)

    def run_simulation(self):
        app_path = self.app_path_input.text().strip()
        start_time_text = self.start_time_input.text().strip()
        stop_time_text = self.stop_time_input.text().strip()

        command = [
            app_path,
            f"-override=startTime={start_time_text},stopTime={stop_time_text}"
        ]

        self.run_button.setEnabled(False)
        self.run_button.setText("Running...")

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(app_path)
        )

        if result.returncode == 0:
            QMessageBox.information(
                self,
                "Success",
                "Simulation completed successfully!"
            )
        else:
            QMessageBox.warning(
                self,
                "Simulation Error",
                f"Simulation finished with errors:\n{result.stderr}"
            )

        self.run_button.setEnabled(True)
        self.run_button.setText("Run Simulation")

def main():
    app = QApplication(sys.argv)
    window = SimulationApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()