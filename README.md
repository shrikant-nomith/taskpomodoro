# Pomodoro Productivity Suite

A comprehensive productivity application that combines a Pomodoro timer with task management, progress tracking, and resource organization features.

## Features

- **Pomodoro Timer**: 25-minute work sessions with 5-minute breaks
- **Task Management**: Add tasks with deadlines and track completion
- **Progress Tracking**: Visualize progress with line graphs and pie charts
- **Resource Management**: Organize reading materials, practice resources, and important links

## Installation

### Option 1: Using the Executable (Recommended for Windows users)

1. Download the latest release from the [Releases](https://github.com/yourusername/pomodoro-productivity-suite/releases) page
2. Run the executable file

### Option 2: From Source

1. Make sure you have Python 3.7 or higher installed
2. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/pomodoro-productivity-suite.git
   cd pomodoro-productivity-suite
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

### Option 3: Using pip

```bash
pip install pomodoro-productivity-suite
pomodoro
```

## Usage

1. **Pomodoro Timer Tab**:

   - Start/Pause/Reset the timer
   - Track work and break sessions

2. **Tasks Tab**:

   - Add new tasks with deadlines (format: YYYY-MM-DD)
   - Mark tasks as complete
   - Delete tasks
   - View days remaining for each task

3. **Progress Tab**:

   - View line graph showing task completion over time
   - See pie chart of completed vs. remaining tasks

4. **Resources Tab**:
   - Add reading materials, practice resources, and important links
   - Organize resources by category
   - Open resources directly from the application

## Data Persistence

All your tasks, resources, and progress are automatically saved to `pomodoro_data.json` in the application directory.

## Building the Executable

If you want to build the executable yourself:

1. Install PyInstaller:

   ```bash
   pip install pyinstaller
   ```

2. Build the executable:
   ```bash
   pyinstaller --onefile --windowed main.py
   ```

The executable will be created in the `dist` folder.

## Requirements

- Python 3.7+
- tkinter (usually comes with Python)
- matplotlib
- Pillow

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
