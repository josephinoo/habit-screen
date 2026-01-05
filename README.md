# Habit Screen 🌿

**Habit Screen** is a minimalist wallpaper generator for macOS. It visualizes your daily habits in a simple grid and automatically updates your desktop background to keep you motivated.

## ✨ Features

- **🎨 Minimalist Aesthetics**: Clean, dark-themed design with a "Dracula" inspired color palette.
- **📊 Visual Progress**: Visualizes your consistency using a simple grid.
- **🖥️ Auto-Update**: Automatically sets the generated image as your macOS wallpaper.
- **Smart Caching**: Uses unique filenames to ensure macOS updates the background immediately.
- **Customizable**: Easy to tweak colors, text, and grid size in the code.

## Prerequisites

- macOS (required for the auto-wallpaper setting feature)
- Python 3
- `Pillow` library

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/habit-screen.git
    cd habit-screen
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    # OR if using uv
    uv pip install -r requirements.txt
    ```

3.  **Make the helper script executable**:
    ```bash
    chmod +x set_wallpaper.sh
    ```

## Usage

The project now includes a powerful CLI tool `habit-screen`.

### 1. List Habits
View all your tracked habits in a clean table:
```bash
./habit-screen list
```

### 2. Track a Habit
Mark a habit as done for today:
```bash
./habit-screen now "read-bible"
```
If you only have one active habit, you can just run:
```bash
./habit-screen now
```
This will automatically update your wallpaper.

### 3. Add a New Habit
Start tracking something new:
```bash
./habit-screen add "workout" --title "WORKOUT" --subtitle "2025 Goals"
```

### 4. Switch Active Habit
Change which habit is displayed on your wallpaper without tracking today:
```bash
./habit-screen switch "workout"
```

## Customization

You can modify the `main` function call at the bottom of `generate_wallpaper.py` to change the title and subtitle:

```python
if __name__ == "__main__":
    # ... load dates ...
    main("READ BIBLE", "Last 365 Days", dates)
```

## Troubleshooting

### Wallpaper not changing?
macOS requires permission for scripts to control the desktop.
1.  Go to **System Settings** > **Privacy & Security** > **Automation**.
2.  Ensure your terminal (iTerm, VS Code, Terminal) has permission to control **System Events** or **Finder**.

### "Bash script failed" error?
Ensure `set_wallpaper.sh` is executable:
```bash
chmod +x set_wallpaper.sh
```

## License
MIT
