Project Setup Checklist
Update Script:

Modify create_project_structure for Flask.
Add folders: templates, uploads, static.
Add files: app.py, upload.html, requirements.txt.
Run Script:

Save as setup_script.py.
Run: python setup_script.py.
Follow prompts: Name, Type (flask), Overwrite (n), Install deps (y).
Add Flask Code:

Update app.py with project logic.
Update upload.html with upload form.
Add any extra files (e.g., config.yaml).
Test Locally:

Activate venv: source venv/bin/activate (Linux/macOS) or .\venv\Scripts\activate (Windows).
Install deps: pip install -r requirements.txt.
Run app: python app.py.
Test at http://127.0.0.1:5000.
Commit & Push:

Stage: git add .
Commit: git commit -m "Initial commit".
Push: git push origin main.
GitHub Actions:

Create .github/workflows/test.yml for CI.
Commit & push: git add .github/workflows/test.yml.
Deploy App:

Google Cloud: gcloud run deploy.
Heroku: git push heroku main.
Update README:

Add description, features, setup, usage, deployment.
Commit & push: git add README.md.