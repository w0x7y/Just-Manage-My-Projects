import json as Json
import subprocess as Subprocess
from pathlib import Path

Projects = Path("./Projects")
template_path = Projects / "project_template.json"
TempletDictionary = {}

def WelcomeScreen():
    print("    0. Reload project template\n    1. Create a new project\n    2. List existing projects\n    3. Update a project\n    4. Delete a project\n    5. Exit")

    choice = input("Enter your choice (0-5): ")
    ActionForChoice(choice)

def ActionForChoice(choice):
    if choice == "0":
        ReloadProjectTemplate()
    elif choice == "1":
        CreateNewProject()
    elif choice == "2":
        ListExistingProjects()
    elif choice == "3":
        UpdateProject()
    elif choice == "4":
        DeleteProject()
    elif choice == "5":
        print("Exiting the program. Goodbye!")
        exit()
    else:
        print("Invalid choice. Please try again.\n")
        WelcomeScreen()

def ReloadProjectTemplate():
    if not template_path.exists():
        template_path.touch()
        DefaultContext = {
            "readme": True,
            "init-git-repo": False
        }
        with open(template_path, "w", encoding="utf-8") as f:
            Json.dump(DefaultContext, f, indent=2)
        print("Project template created and reloaded\n")
        ProjectTemplateChecks()
    else:
        print("Your project template has been reloaded successfully.")
        ProjectTemplateChecks()
    WelcomeScreen()

def ProjectTemplateChecks():
    global TempletDictionary
    
    TempletDictionary.clear()
    
    with open(template_path, "r", encoding="utf-8") as f:
        data = Json.load(f)

    for key, value in data.items():
        TempletDictionary[key] = value

    print("Current template settings:\n")
    for key, value in TempletDictionary.items():
        print(f"{key}: {value}")
    print("\n")

def CreateNewProject():
    project_name = input("Enter the name of the new project: ")
    project_path = Projects / project_name

    if project_path.exists():
        print(f"A project named '{project_name}' already exists. Please choose a different name.\n")
        CreateNewProject()
    else:
        project_path.mkdir(parents=True, exist_ok=True)
        for key, value in TempletDictionary.items():
            if key == "readme" and value:
                readme_path = project_path / "README.md"
                readme_path.touch()
            elif key == "init-git-repo" and value:
                gitignore_path = project_path / ".gitignore"
                gitignore_path.touch()
                
                Subprocess.run(["git", "init", str(project_path)])
                Subprocess.run(["git", "add", "."], cwd=project_path)
                Subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=project_path)
        print(f"Project '{project_name}' created successfully!\n")
        WelcomeScreen()

def ListExistingProjects():
    count = 1
    print("Listing existing projects...")
    for item in Projects.iterdir():
        print(f"{count}. {item.name}")
        count += 1
    WelcomeScreen()

def main():
    print("Welcome to Just Manage My Projects!")
    print("What would you like to do?")
    WelcomeScreen()


if __name__ == "__main__":
    main()
