import json
import re
import shutil
import subprocess
import os
from pathlib import Path
from DEFAULTS import defaults

# Characters that are invalid in folder names on Windows/macOS/Linux
INVALID_NAME_CHARS = set('<>:"/\\|?*')

DEFAULT_FILE_CONTENTS = {
    "TODO.md": defaults.DEFAULT_TODO_TEMPLATE,
    "Issues.json": json.dumps(defaults.DEFAULT_ISSUES_TRACKER, indent=2),
    "Project.json": json.dumps(defaults.DEFAULT_PROJECT_METADATA, indent=2),
    "index.html": defaults.DEFAULT_PROJECT_INDEX_HTML,
}

class ProjectManager:
    def __init__(self, projects_dir: Path = Path("./Projects")):
        self.projects_dir = projects_dir
        self.template_path = self.projects_dir / "project_template.json"
        self.template = {}

        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.load_template()
        self.regenerate_webui()

    # Menu / control flow
    def run(self):
        print("Welcome to Just Manage My Projects!")
        print("What would you like to do?")

        while True:
            choice = self.show_menu()
            if not self.handle_choice(choice):
                break

    def show_menu(self) -> str:
        print(
            "    0. Reload project template\n"
            "    1. Create a new project\n"
            "    2. List existing projects\n"
            "    3. Update a project (If a remote Git repo is present)\n"
            "    4. Delete a project\n"
            "    5. View/Edit projects\n"
            "    6. Change default editor (current: {})\n".format(defaults.EDITOR) +
            "    7. Exit"
        )
        return input("Enter your choice (0-7): ").strip()

    def handle_choice(self, choice: str) -> bool:
        """Returns False when the program should exit."""
        actions = {
            "0": self.reload_template,
            "1": self.create_new_project,
            "2": self.list_existing_projects,
            "3": self.update_project,
            "4": self.delete_project,
            "5": self.view_projects,
            "6": self.change_default_editor,
        }

        if choice == "7":
            self.clear_terminal()
            
            print("Exiting. Goodbye!")
            return False

        action = actions.get(choice)
        if action is None:
            print("Invalid choice. Please try again.\n")
        else:
            action()

        return True


    def clear_terminal(self):
        if os.name == "nt":
            subprocess.run(["cmd", "/c", "cls"])
        else:
            self.clear_terminal()

    # Template handling
    def reload_template(self):
        self.clear_terminal()

        if not self.template_path.exists():
            self._create_default_template()
            print("Project template created and reloaded\n")
        else:
            print("Your project template has been reloaded successfully.")

        self.load_template()

    def _create_default_template(self):
        with open(self.template_path, "w", encoding="utf-8") as f:
            json.dump(defaults.DEFAULT_TEMPLATE, f, indent=2)

    def load_template(self):
        """Loads the template from disk, creating a default one if missing
        or unreadable. Safe to call anytime (lazy-load)."""
        if not self.template_path.exists():
            self._create_default_template()

        try:
            with open(self.template_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Warning: couldn't read template ({e}). Using defaults.\n")
            data = defaults.DEFAULT_TEMPLATE

        # Merge with defaults so missing keys don't silently break things
        self.template = {
            "files": {**defaults.DEFAULT_TEMPLATE["files"], **data.get("files", {})},
            "folders": {**defaults.DEFAULT_TEMPLATE["folders"], **data.get("folders", {})},
            "init-git-repo": data.get("init-git-repo", False),
        }

        print("Current template settings:\n")
        print(f"folders: {self.template['folders']}")
        print(f"files: {self.template['files']}")
        print(f"init-git-repo: {self.template['init-git-repo']}")
        print()

    # WebUI syncing
    def regenerate_webui(self):
        """Rewrites the auto-generated project list inside WebUI.html so it
        always reflects the folders currently in the Projects directory.
        Recreates WebUI.html and styles.css from defaults if either was
        deleted, the same way project_template.json gets recreated."""
        webui_path = self.projects_dir / "WebUI.html"
        styles_path = self.projects_dir / "styles.css"

        if not styles_path.exists():
            styles_path.write_text(defaults.DEFAULT_STYLES_CSS, encoding="utf-8")
            print("styles.css was missing, so it was recreated.\n")

        if not webui_path.exists():
            webui_path.write_text(defaults.DEFAULT_WEBUI_HTML, encoding="utf-8")
            print("WebUI.html was missing, so it was recreated.\n")

        project_names = sorted(
            item.name for item in self.projects_dir.iterdir() if item.is_dir()
        )

        if project_names:
            entries = ",\n".join(
                f"                    {{ name: {json.dumps(name)}, path: {json.dumps(name)} }}"
                for name in project_names
            )
            block = f"const projects = [\n{entries},\n                ];"
        else:
            block = "const projects = [];"

        try:
            html = webui_path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"Warning: couldn't read WebUI.html ({e}). Skipping sync.\n")
            return

        pattern = re.compile(
            r"(// AUTO-GENERATED-PROJECTS-START\n)(.*?)(\n\s*// AUTO-GENERATED-PROJECTS-END)",
            re.DOTALL,
        )
        if not pattern.search(html):
            print(
                "Warning: couldn't find the AUTO-GENERATED-PROJECTS markers in "
                "WebUI.html. Skipping sync.\n"
            )
            return

        new_html = pattern.sub(
            lambda m: m.group(1) + "                " + block + m.group(3),
            html,
        )

        try:
            webui_path.write_text(new_html, encoding="utf-8")
        except OSError as e:
            print(f"Warning: couldn't write WebUI.html ({e}).\n")

    # Project actions
    def _is_valid_project_name(self, name: str) -> bool:
        if not name or not name.strip():
            return False
        if name != name.strip():
            # leading/trailing whitespace
            return False
        if any(char in INVALID_NAME_CHARS for char in name):
            return False
        return True

    def create_new_project(self):
        self.clear_terminal()
        
        while True:
            project_name = input("Enter the name of the new project: ")

            if not self._is_valid_project_name(project_name):
                print(
                    "Invalid project name. Names can't be empty, "
                    "have leading/trailing spaces, or contain: "
                    f"{' '.join(INVALID_NAME_CHARS)}\n"
                )
                continue

            project_path = self.projects_dir / project_name
            if project_path.exists():
                print(
                    f"A project named '{project_name}' already exists. "
                    "Please choose a different name.\n"
                )
                continue

            break

        # Lazy-load in case the template was never loaded/reloaded
        if not self.template:
            self.load_template()

        project_path.mkdir(parents=True)

        for foldername, should_create in self.template.get("folders", {}).items():
            if should_create:
                (project_path / foldername).mkdir()

        for filename, should_create in self.template.get("files", {}).items():
            if should_create:
                file_path = project_path / filename
                default_content = DEFAULT_FILE_CONTENTS.get(filename)
                if default_content is not None:
                    file_path.write_text(default_content, encoding="utf-8")
                else:
                    file_path.touch()

        if self.template.get("init-git-repo"):
            self._init_git_repo(project_path)

        self.regenerate_webui()
        print(f"Project '{project_name}' created successfully!\n")

    def _init_git_repo(self, project_path: Path):
        if shutil.which("git") is None:
            print("Warning: git is not installed or not on PATH. Skipping git init.\n")
            return

        steps = [
            (["git", "init"], "initialize git repository"),
            (["git", "add", "."], "stage files"),
            (["git", "commit", "-m", "Initial commit"], "create initial commit"),
        ]

        for command, description in steps:
            result = subprocess.run(
                command,
                cwd=project_path,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                print(
                    f"Warning: failed to {description}. Git said:\n{result.stderr.strip()}\n"
                )
                return

    def list_existing_projects(self):
        self.clear_terminal()
        
        print("Listing existing projects...")
        projects = [item for item in self.projects_dir.iterdir() if item.is_dir()]

        if not projects:
            print("No projects found.\n")
            return

        for count, item in enumerate(projects, start=1):
            print(f"{count}. {item.name}")
        print()

    def update_project(self):
        self.clear_terminal()
        
        # TODO: implement project updating
        print("Update project is not implemented yet — coming soon!\n")

    def delete_project(self):
        self.clear_terminal()
        
        project_name = input("Enter the name of the project to delete: ")
        project_path = self.projects_dir / project_name

        if not project_path.exists() or not project_path.is_dir():
            print(f"No project named '{project_name}' found.\n")
            return

        confirmation = (
            input(
                f"Are you sure you want to delete the project '{project_name}'? (y/n): "
            )
            .strip()
            .lower()
        )

        if confirmation == "y":
            shutil.rmtree(project_path)
            self.regenerate_webui()
            print(f"Project '{project_name}' has been deleted.\n")
        else:
            print("Deletion canceled.\n")

    def change_default_editor(self):
        self.clear_terminal()
        
        new_editor = input(
            f"Enter the command for your preferred text editor (current: {defaults.EDITOR}): "
        ).strip()
        if new_editor:
            defaults.EDITOR = new_editor
            print(f"Default editor changed to: {defaults.EDITOR}\n")
        else:
            print("No changes made to the default editor.\n")

    def view_projects(self):
        self.clear_terminal()
        
        project_name = input("Choose a project by entering the name: ")
        project_path = self.projects_dir / project_name

        if not project_path.exists() or not project_path.is_dir():
            print(f"No project named '{project_name}' found.\n")
            return

        for item in project_path.iterdir():
            if item.is_dir():
                print(f"Folder: {item.name}")

        for item in project_path.iterdir():
            if item.is_file() and not item.name == "index.html":
                print(f"File: {item.name}")

        file_to_open = input("Enter the name of the file you want to open (or press Enter to skip): ").strip()
        if file_to_open:
            file_path = project_path / file_to_open
            if file_path.exists() and file_path.is_file():
                print(f"Opening file: {file_to_open}")
                try:
                    subprocess.run([defaults.EDITOR, str(file_path)], check=True)
                    print(f"Successfully edited {file_path}")
                except FileNotFoundError:
                    print(f"Error: '{defaults.EDITOR}' is not installed or not in your system's PATH.")
                except subprocess.CalledProcessError:
                    print(f"{defaults.EDITOR} closed with an error code.")
            else:
                print(f"File not found: {file_to_open}\n canceling operation.\n")

def main():
    manager = ProjectManager()
    manager.run()


if __name__ == "__main__":
    main()
