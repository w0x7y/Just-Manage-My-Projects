import json
import shutil
import subprocess
from pathlib import Path

# Characters that are invalid in folder names on Windows/macOS/Linux
INVALID_NAME_CHARS = set('<>:"/\\|?*')

DEFAULT_TEMPLATE = {
    "files": {
        "README.md": True,
        ".gitignore": False,
    },
    "init-git-repo": False,
}


class ProjectManager:
    def __init__(self, projects_dir: Path = Path("./Projects")):
        self.projects_dir = projects_dir
        self.template_path = self.projects_dir / "project_template.json"
        self.template = {}

        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.load_template()

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
            "    3. Update a project\n"
            "    4. Delete a project\n"
            "    5. Exit"
        )
        return input("Enter your choice (0-5): ").strip()

    def handle_choice(self, choice: str) -> bool:
        """Returns False when the program should exit."""
        actions = {
            "0": self.reload_template,
            "1": self.create_new_project,
            "2": self.list_existing_projects,
            "3": self.update_project,
            "4": self.delete_project,
        }

        if choice == "5":
            print("Exiting the program. Goodbye!")
            return False

        action = actions.get(choice)
        if action is None:
            print("Invalid choice. Please try again.\n")
        else:
            action()

        return True

    # Template handling
    def reload_template(self):
        if not self.template_path.exists():
            self._create_default_template()
            print("Project template created and reloaded\n")
        else:
            print("Your project template has been reloaded successfully.")

        self.load_template()

    def _create_default_template(self):
        with open(self.template_path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_TEMPLATE, f, indent=2)

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
            data = DEFAULT_TEMPLATE

        # Merge with defaults so missing keys don't silently break things
        self.template = {
            "files": {**DEFAULT_TEMPLATE["files"], **data.get("files", {})},
            "init-git-repo": data.get("init-git-repo", False),
        }

        print("Current template settings:\n")
        print(f"files: {self.template['files']}")
        print(f"init-git-repo: {self.template['init-git-repo']}")
        print()

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

        for filename, should_create in self.template.get("files", {}).items():
            if should_create:
                (project_path / filename).touch()

        if self.template.get("init-git-repo"):
            self._init_git_repo(project_path)

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
        print("Listing existing projects...")
        projects = [item for item in self.projects_dir.iterdir() if item.is_dir()]

        if not projects:
            print("No projects found.\n")
            return

        for count, item in enumerate(projects, start=1):
            print(f"{count}. {item.name}")
        print()

    def update_project(self):
        # TODO: implement project updating
        print("Update project is not implemented yet — coming soon!\n")

    def delete_project(self):
        project_name = input("Enter the name of the project to delete: ")
        project_path = self.projects_dir / project_name

        if not project_path.exists() or not project_path.is_dir():
            print(f"No project named '{project_name}' found.\n")
            return

        confirmation = input(
            f"Are you sure you want to delete the project '{project_name}'? (y/n): "
        ).strip().lower()

        if confirmation == "y":
            shutil.rmtree(project_path)
            print(f"Project '{project_name}' has been deleted.\n")
        else:
            print("Deletion canceled.\n")

def main():
    manager = ProjectManager()
    manager.run()


if __name__ == "__main__":
    main()
