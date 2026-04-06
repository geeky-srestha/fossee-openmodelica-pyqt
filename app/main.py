import sys
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

def main():
    app = QApplication(sys.argv)
    window = SimulationApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()