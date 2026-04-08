import sys
import os
import subprocess
from PyQt6.QtWidgets import (
    QApplication,
    QGroupBox,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QTextCursor


class SimulationApp(QMainWindow):
    """Main window for the TwoConnectedTanks simulation launcher."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenModelica Simulation Launcher")
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        self.setAcceptDrops(True)
        self.setup_ui()
        # self.apply_styles()

    def setup_ui(self):
        """Set up all UI components."""

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        central_widget.setLayout(main_layout)

        # Title
        title_label = QLabel("OpenModelica Simulation Launcher")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Input Group Box
        input_group = QGroupBox("Simulation Parameters")
        input_layout = QVBoxLayout()
        input_layout.setSpacing(8)
        input_group.setLayout(input_layout)

        # Input Field 1: Application path
        app_label = QLabel("Simulation Executable:")
        self.app_path_input = QLineEdit()
        self.app_path_input.setPlaceholderText("Select the TwoConnectedTanks executable...")
        browse_button = QPushButton("  Browse")
        browse_button.setFixedWidth(80)
        browse_button.setIcon(QIcon.fromTheme("folder-open"))
        browse_button.clicked.connect(self.browse_executable)

        app_row = QHBoxLayout()
        app_row.addWidget(self.app_path_input)
        app_row.addWidget(browse_button)

        # Input Field 2: Start Time
        start_label = QLabel("Start Time (integer, >= 0):")
        self.start_time_input = QLineEdit()
        self.start_time_input.setPlaceholderText("e.g. 0")
        browse_button.setFixedWidth(80)
        self.start_time_input.setFixedWidth(100)

        # Input Field 3: Stop Time
        stop_label = QLabel("Stop Time (integer, < 5):")
        self.stop_time_input = QLineEdit()
        self.stop_time_input.setPlaceholderText("e.g. 3")
        self.stop_time_input.setFixedWidth(100)

        # Run Button
        self.run_button = QPushButton("  Run Simulation")
        self.run_button.setIcon(QIcon.fromTheme("media-playback-start"))
        self.run_button.setFixedHeight(45)
        self.run_button.clicked.connect(self.run_simulation)

        # added everything to main layout
        input_layout.addWidget(app_label)
        input_layout.addLayout(app_row)
        input_layout.addWidget(start_label)
        input_layout.addWidget(self.start_time_input)
        input_layout.addWidget(stop_label)
        input_layout.addWidget(self.stop_time_input)
        main_layout.addSpacing(10)
        main_layout.addWidget(input_group)
        self.status_label = QLabel("Status: Ready")
        main_layout.addWidget(self.status_label)

        # Output box to display simulation logs
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Simulation output will appear here...")
        main_layout.addWidget(self.output_box)

        main_layout.addWidget(self.run_button)


    def browse_executable(self):
        """Open file dialog to select the simulation executable."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Simulation Executable",
            "",
            "Executable Files (*.exe *.bat)"
        )
        if file_path:
            self.app_path_input.setText(file_path)

    def run_simulation(self):
        """Validate inputs and run the simulation executable."""

        # Get values from all three input fields
        self.output_box.clear()
        app_path = self.app_path_input.text().strip()
        start_time_text = self.start_time_input.text().strip()
        stop_time_text = self.stop_time_input.text().strip()
        step_size = (int(stop_time_text) - int(start_time_text)) / 500


        # condition to check nothing is empty
        if not app_path:
            QMessageBox.warning(self, "Missing Input", "Please select a simulation executable.")
            return

        if not start_time_text:
            QMessageBox.warning(self, "Missing Input", "Please enter a start time.")
            return

        if not stop_time_text:
            QMessageBox.warning(self, "Missing Input", "Please enter a stop time.")
            return
        # Check that start and stop are integers
        try:
            start_time = int(start_time_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Start time must be an integer.")
            return

        try:
            stop_time = int(stop_time_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Stop time must be an integer.")
            return

         # Check the condition: 0 <= start < stop < 5
        if not (0 <= start_time < stop_time < 5):
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Times must satisfy: 0 <= Start Time < Stop Time < 5"
            )
            return

        if app_path.endswith(".exe"):
           bat_path = app_path.replace(".exe", ".bat")
           if os.path.exists(bat_path):
              app_path = bat_path

        # Build the command and run it by passing the start and stop time as arguments to the executable
        command = [
           app_path,
           f"-startTime={start_time}",
           f"-stopTime={stop_time}",
           f"-stepSize={step_size}",
           "-lv=LOG_STATS"
        ]

        try:
            self.status_label.setText("Status: Running...")
            self.run_button.setEnabled(False)
            self.run_button.setText("Running...")

            result = subprocess.run(
                command,  #command running the executable with the arguments
                capture_output=True,
                text=True,
                cwd=os.path.dirname(app_path)
            )
            # Display stdout in output box
            if result.stdout:
                self.output_box.setText(result.stdout)
                self.output_box.moveCursor(QTextCursor.MoveOperation.End)

            if result.returncode == 0:
                self.status_label.setText("Status: Completed ✅")
                QMessageBox.information(
                    self,
                    "Success",
                    "Simulation completed successfully!"
                )
            else:
                self.status_label.setText("Status: Error ❌")
                if result.stderr:
                    self.output_box.setText(result.stderr)
                    self.output_box.moveCursor(QTextCursor.MoveOperation.End)
                QMessageBox.warning(
                    self,
                    "Simulation Error",
                    f"Simulation finished with errors:\n{result.stderr}"
                )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to run simulation:\n{str(e)}")

        finally:
            self.run_button.setEnabled(True)
            self.run_button.setText("Run Simulation")

    #drag and drop functionality to allow users to drag the executable file into the application
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.endswith(".exe") or file_path.endswith(".bat"):
                    self.app_path_input.setText(file_path)
                    self.status_label.setText(f"Status: Executable loaded via drag & drop ✅")
                    break


def main():
    app = QApplication(sys.argv)
    window = SimulationApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()