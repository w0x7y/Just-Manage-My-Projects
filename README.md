# Just Manage My Projects 📋

A simple and efficient CLI-based project management tool that allows you to create, organize, and manage your projects and tasks from the command line.

## Features ✨

- **Create New Projects** - Quickly scaffold new projects with customizable templates
- **List Projects** - View all your existing projects at a glance
- **Update Projects** - Modify project settings and configurations
- **Delete Projects** - Remove projects you no longer need
- **Project Templates** - Define default settings for all new projects (README generation, git initialization)
- **Git Integration** - Optionally initialize git repositories for your projects automatically

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

### Menu Options

```
0. Reload project template - Reload or create the default project template
1. Create a new project - Create a new project from the template
2. List existing projects - View all your projects
3. Update a project - Modify an existing project (coming soon)
4. Delete a project - Remove a project (coming soon)
5. Exit - Close the application
```

## How It Works 🔧

### Project Template
When you first run the application, a `project_template.json` file is created in the `Projects` directory. This file controls default settings for new projects:

```json
{
  "files": {
    "README.md": true,
    ".gitignore": false
  },
  "init-git-repo": false
}
```

- `files`: A dictionary of filenames to create in each new project. Set any filename to `true` to have it created automatically (empty), or `false` to skip it. You can add your own entries here (e.g. `"LICENSE": true`) to have them created for every new project.
- `init-git-repo`: If `true`, a git repository is automatically initialized with an initial commit. If `git` isn't installed or a git command fails, you'll get a warning instead of a silent failure.

### Creating a Project
1. Select option `1` from the main menu
2. Enter the project name (it can't be empty, have leading/trailing spaces, or contain invalid filesystem characters like `< > : " / \ | ? *`)
3. The project will be created in the `Projects/` directory with the specified template settings

### Project Directory Structure
```
Projects/
├── project_template.json
├── Your Project 1/
│   └── README.md
├── Your Project 2/
│   ├── README.md
│   └── .git/
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
    ├── project_template.json
    └── [your projects here]
```

## Configuration 🔨

Edit `Projects/project_template.json` to customize default behavior for new projects:

```json
{
  "files": {
    "README.md": true,
    ".gitignore": true
  },
  "init-git-repo": true
}
```

Then reload the template using option `0` in the menu.

## Development 🛠️

This project uses:
- **Python 3.13+** - Core language
- **pathlib** - Cross-platform file handling
- **json** - Configuration management
- **subprocess** - Git integration

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

## Future Enhancements 🚀

- [ ] Update project functionality
- [x] Delete project functionality
- [x] Project metadata
- [ ] Task management within projects
- [ ] Project statistics and analytics
- [ ] Web-based interface
- [ ] Export project information

## License 📄

This project is open source and available under the MIT License.

## Contributing 🤝

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

## Support 💬

If you have any questions or issues, please create an issue in the repository.
