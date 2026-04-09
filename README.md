# 🧪 OpenModelica Simulation Launcher

A desktop GUI application built with **Python** and **PyQt6** that allows users to run OpenModelica-compiled simulation executables with configurable start and stop time parameters.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Input Validation Rules](#input-validation-rules)
- [Screenshots](#screenshots)
- [Technologies Used](#technologies-used)
- [Author](#author)

---

## 📖 Overview

This project is a two-part task:

1. **Compile** the `TwoConnectedTanks` model in OpenModelica to produce a simulation executable.
2. **Launch** that executable through a user-friendly PyQt6 desktop application, passing simulation parameters (start time, stop time, step size) as command-line arguments.

The GUI abstracts away the command-line complexity and gives users an intuitive interface to configure and run OpenModelica simulations.

---

## ✨ Features

- 📂 **Browse or drag-and-drop** a simulation executable (`.exe` or `.bat`) into the app
- ⏱️ **Configurable start and stop times** with full input validation
- ▶️ **One-click simulation** via the Run button or `Ctrl+R` shortcut
- 📋 **Live output log** — stdout from the simulation is displayed in the app
- ✅ **Status indicator** — shows Ready / Running / Completed / Error states
- 🛠️ **Toolbar** with Open, Run, About, and Exit actions (keyboard shortcuts included)
- 💬 **About dialog** with application information
- 🎨 Clean, grouped UI layout with clear labelling

---

## 📁 Project Structure

```
fossee-openmodelica-pyqt/
│
├── app/                  # Main application source code
│   ├── main.py
│   ├── icons/                   # Toolbar and window icons
│   │   ├── app_icon.png
│   │   ├── open.png
│   │   ├── run.png
│   │   ├── exit.png
│   │   └── info.png
├── simulation_files/       # Compiled OpenModelica executable and dependencies
│   ├── TwoConnectedTanks.exe   (Windows) / TwoConnectedTanks (Linux)
│   ├── TwoConnectedTanks.bat   (Windows launcher script, if applicable)
│   └── ...                  # Other runtime libraries and model files
├── requirements.txt         # Python dependencies
└── README.md
```

---

## ✅ Prerequisites

- Python 3.6 or higher
- [OpenModelica](https://openmodelica.org/) (for building the simulation executable)
- pip (Python package manager)

---

## 🔧 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/geeky-srestha/fossee-openmodelica-pyqt.git
   cd fossee-openmodelica-pyqt
   ```

2. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   Or manually:

   ```bash
   pip install PyQt6
   ```
---

## ▶️ Running the Application

```bash
python main.py
```

---

## 🖱️ Usage Guide

1. **Select the Executable** — Click **Browse** (or drag and drop a `.exe`/`.bat` file onto the window) to choose the `TwoConnectedTanks` executable.
2. **Enter Start Time** — Type an integer start time (must be ≥ 0).
3. **Enter Stop Time** — Type an integer stop time (must be > start time and < 5).
4. **Click "Run Simulation"** — The app will execute the simulation and stream the output log into the output panel.
5. The **status bar** updates to reflect the current state: `Ready`, `Running...`, `Completed ✅`, or `Error ❌`.

### Keyboard Shortcuts

| Action           | Shortcut  |
|------------------|-----------|
| Open Executable  | `Ctrl+O`  |
| Run Simulation   | `Ctrl+R`  |
| About            | `Ctrl+I`  |
| Exit             | `Ctrl+Q`  |

---

## 🔒 Input Validation Rules

The application enforces the following before running the simulation:

- All three fields (executable path, start time, stop time) must be filled.
- Start time and stop time must be **integers** (not floats or strings).
- The following condition must hold: `0 <= Start Time < Stop Time < 5`

Any violation will trigger a descriptive warning dialog before execution.

---

## 📸 Screenshots


---

## 🛠️ Technologies Used

| Technology     | Purpose                              |
|----------------|--------------------------------------|
| Python 3.6+    | Core programming language            |
| PyQt6          | GUI framework                        |
| OpenModelica   | Model compilation and simulation     |
| subprocess     | Launching the simulation executable  |

---

## 👤 Author

**Srestha Kumar**  
Built as part of the FOSSEE OpenModelica Screening Task
For queries, reach out to: connect.srestha@gmail.com
