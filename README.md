# Just Manage My Projects 📋

A simple and efficient CLI-based project management tool that allows you to create, organize, and manage your projects and tasks from the command line.

## Features ✨

- **Create New Projects** - Quickly scaffold new projects with customizable templates
- **List Projects** - View all your existing projects at a glance
- **Update Projects** - Upgrade the project to a new version if available on github (if a GitHub repository is associated with the project)
- **Delete Projects** - Remove projects you no longer need
- **Project Templates** - Define default settings for all new projects (README generation, git initialization, TODO list, etc.)
- **Git Integration** - Optionally initialize git repositories for your projects automatically
- **Web-based Interface** - Manage your projects through a simple web interface (WIP)

## Requirements 📦

- Python 3.13 or higher

## Installation 🚀

1. Clone or download this repository
2. Ensure you have Python 3.13+ installed
3. Install dependencies using `uv` (if needed):
   ```bash
   uv sync
   ```

## Usage 🎯

Start the application:
```bash
python main.py
```

## How It Works 🔧

### Project Template
When you first run the application, a `project_template.json` file is created in the `Projects` directory. This file controls default settings for new projects:

```json
{
    "folders": {
        "src": True,  # src is a folder for source code
    },
    "files": {
        "index.html": True,  # index.html is a file for the webUI manager
        "Notes.md": False,  # Notes.md is a file for taking free-form notes
        "Project.json": True,  # Project.json is a file for storing project metadata
        "Issues.json": True,  # Issues.json is a file for tracking issues
        "TODO.md": True,  # TODO.md is a file for tracking tasks
        "README.md": True,  # README.md is a file for project documentation
        ".gitignore": False,
    },
    "init-git-repo": False,
}
```

### Creating a Project
1. Select option `1` from the main menu
2. Enter the project name (it can't be empty, have leading/trailing spaces, or contain invalid filesystem characters like `< > : " / \ | ? *`)
3. The project will be created in the `Projects/` directory with the specified template settings

### Project Directory Structure
```
Projects/
├── style.css
├── WebUI.html
├── project_template.json
├── Your Project 1/
│   └── Your Project 1 Files...
├── Your Project 2/
│   └── Your Project 2 Files...
└── ...
```

## Project Structure 📁

```
.
├── main.py                 # Main application entry point
├── pyproject.toml          # Project metadata and dependencies
├── uv.lock                 # Dependency lock file
├── README.md              # This file
├── .gitignore             # Git ignore rules
├── .python-version        # Python version specification
├── .venv/                 # Virtual environment (local)
└── Projects/              # Directory containing all your projects
```

## Configuration 🔨

Edit `Projects/project_template.json` to customize default behavior for new projects:

```json
{
    "folders": {
        "src": True,  # src is a folder for source code
    },
    "files": {
        "index.html": True,  # index.html is a file for the webUI manager
        "Notes.md": False,  # Notes.md is a file for taking free-form notes
        "Project.json": True,  # Project.json is a file for storing project metadata
        "Issues.json": True,  # Issues.json is a file for tracking issues
        "TODO.md": True,  # TODO.md is a file for tracking tasks
        "README.md": True,  # README.md is a file for project documentation
        ".gitignore": False,
    },
    "init-git-repo": False,
}
```

Then reload the template using option `0` in the menu.

## Development 🛠️

This project uses:
- **Python 3.13+** - Core language
- **pathlib** - Cross-platform file handling
- **json** - Configuration management
- **subprocess** - Git integration
- **re** - Input validation
- **shutil** - File and directory operations
- **uv** - Dependency management

### Running from Source

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Run the application
python main.py
```

## Future 🚀

- [ ] Auto getting the project information from GitHub (if a GitHub repository is associated with the project)
- [ ] Make the CLI part more have more functionality (So the user can just use the CLI without needing to use the Web-based interface or other editors)
- [x] Fixing the TODO list fetching from the file to the Web-based interface
- [ ] Make the Web-based interface more interactive and user-friendly
- [ ] Auto GitHub integration for project updates (fetching newer versions, issues and more)
- [ ] Export project information

## License 📄

This project is open source and available under the MIT License.

## Contributing 🤝

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

## Support 💬

If you have any questions or issues, please create an issue in the repository.
