import os
import hashlib
import subprocess
import venv
import json
from pathlib import Path

def create_file(filepath, content="", overwrite=False):
    """Create or update a file with the given content."""
    try:
        with open(filepath, "r") as f:
            if overwrite:
                existing_content = f.read()
                existing_hash = hashlib.sha256(existing_content.encode()).hexdigest()
                new_hash = hashlib.sha256(content.encode()).hexdigest()
                if existing_hash == new_hash:
                    print(f"File '{filepath}' already exists and content is the same. Skipping.")
                    return
    except FileNotFoundError:
        pass  # File doesn't exist yet; proceed with creation
    except Exception as e:
        print(f"Error checking file '{filepath}': {e}")
        return

    print(f"Updating or creating file '{filepath}'.")
    with open(filepath, "w") as f:
        f.write(content)

def create_and_activate_venv(project_path):
    """Create and activate a virtual environment."""
    venv_dir = os.path.join(project_path, "venv")
    venv.create(venv_dir, with_pip=True)
    print(f"Virtual environment created at {venv_dir}")

    # Activation instructions (platform-specific)
    if os.name == "nt":  # Windows
        activate_script = os.path.join(venv_dir, "Scripts", "activate")
        print(f"Activate venv: {activate_script}")
    else:  # Linux/macOS (Posix)
        activate_script = os.path.join(venv_dir, "bin", "activate")
        print(f"Activate venv: source {activate_script}")

def create_directories(root_dir, folders):
    """Create directories if they don't exist."""
    for folder in folders:
        os.makedirs(os.path.join(root_dir, folder), exist_ok=True)

def create_files(root_dir, files, overwrite=False):
    """Create or update files with the given content."""
    for filepath, content in files.items():
        create_file(os.path.join(root_dir, filepath), content, overwrite)

def delete_unlisted_files(root_dir, allowed_files):
    """Delete files not in the allowed list."""
    for root, _, files in os.walk(root_dir):
        for file in files:
            filepath = os.path.join(root, file)
            relative_path = os.path.relpath(filepath, root_dir)
            if relative_path not in allowed_files:
                try:
                    os.remove(filepath)
                    print(f"Deleted unlisted file: {relative_path}")
                except OSError as e:
                    print(f"Error deleting file {relative_path}: {e}")

def create_flask_app_structure(root_dir):
    """Create the structure for a Flask app."""
    folders = ["templates", "uploads", "static"]
    create_directories(root_dir, folders)

    files = {
        "app.py": """from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/process', methods=['POST'])
def process_files():
    # Add your file processing logic here
    return "Files processed successfully!"

if __name__ == '__main__':
    app.run(debug=True)
""",
        "templates/upload.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload CSV</title>
</head>
<body>
    <h1>Upload CSV Files</h1>
    <form action="/process" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".csv">
        <button type="submit">Upload</button>
    </form>
</body>
</html>
""",
        "requirements.txt": """Flask
pandas
numpy
"""
    }
    create_files(root_dir, files)

def create_data_analysis_structure(root_dir):
    """Create the structure for a data analysis project."""
    folders = ["data/raw", "data/processed", "notebooks", "scripts", "config"]
    create_directories(root_dir, folders)

    files = {
        "README.md": "# Data Analysis Project\n\nProject description goes here.",
        "config/config.yaml": "api_url: 'https://api.example.com'\naccess_token: 'YOUR_ACCESS_TOKEN'",
        "requirements.txt": "pandas\nnumpy\nmatplotlib\n"
    }
    create_files(root_dir, files)

def create_project_structure(project_name, project_type, overwrite=False, install_deps=True):
    """Create a project structure based on the project type."""
    root_dir = os.path.join(os.getcwd(), project_name)

    # Create virtual environment
    create_and_activate_venv(root_dir)

    # Create project structure
    if project_type == "flask":
        create_flask_app_structure(root_dir)
    elif project_type == "data_analysis":
        create_data_analysis_structure(root_dir)
    else:
        print(f"Unknown project type: {project_type}")
        return

    # Clean up unlisted files
    try:
        with open('files_to_keep.json', 'r') as f:
            files_to_keep = json.load(f)
    except FileNotFoundError:
        print("Error: files_to_keep.json not found. Using default list.")
        files_to_keep = ["README.md", "requirements.txt", "app.py", "templates/upload.html"]

    delete_unlisted_files(root_dir, files_to_keep)

    if install_deps:
        print("\nRemember to activate your virtual environment and install any necessary dependencies.")

    print(f"\nProject structure created for '{project_name}' in {root_dir}.")

if __name__ == "__main__":
    project_name = input("Enter project name: ")
    project_type = input("Enter project type (flask/data_analysis): ").lower()
    overwrite = input("Overwrite existing project? (y/n): ").lower() == "y"
    install_deps = input("Install dependencies? (y/n): ").lower() == "y"
    create_project_structure(project_name, project_type, overwrite, install_deps)