from pathlib import Path

APPS = [
    "characters",
    "concepts",
    "core",
    "issues",
    "locations",
    "missing_issues",
    "objects",
    "people",
    "powers",
    "publishers",
    "search",
    "spiders",
    "story_arcs",
    "teams",
    "utils",
    "users",
    "volumes",
]

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs" / "backend"
APPS_DIR = BASE_DIR / "read_comics"
BACKEND_README = DOCS_DIR / "README.md"

missing_docs = []
missing_apps = []
missing_links = []
backend_readme_text = BACKEND_README.read_text()

for app in APPS:
    doc = DOCS_DIR / app / "README.md"
    if not doc.exists():
        missing_docs.append(app)
    app_path = APPS_DIR / app
    if not app_path.exists():
        missing_apps.append(app)
    if f"{app}/README.md" not in backend_readme_text:
        missing_links.append(app)

if missing_docs or missing_apps or missing_links:
    print("Backend documentation check failed")
    if missing_docs:
        print("Missing docs for apps:", ", ".join(missing_docs))
    if missing_apps:
        print("Missing app directories (maybe removed):", ", ".join(missing_apps))
    if missing_links:
        print("Missing README links for apps:", ", ".join(missing_links))
    exit(1)

print("All backend apps have README docs and referenced links.")
