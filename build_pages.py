"""Render the Flask site as static files for GitHub Pages."""

import os
import shutil
from pathlib import Path

from app import app, load_posts, load_projects

ROOT = Path(__file__).parent
OUTPUT = ROOT / "docs"
BASE_PATH = os.environ.get("PAGES_BASE_PATH", "/sarah-portfolio").rstrip("/")


def routes():
    paths = ["/", "/about", "/projects", "/blog", "/contact"]
    paths.extend(f"/projects/{project['slug']}" for project in load_projects())
    paths.extend(f"/blog/{post['slug']}" for post in load_posts())
    return paths


def static_path(path):
    return OUTPUT / ("index.html" if path == "/" else path.strip("/") + "/index.html")


def rewrite_paths(html):
    html = html.replace('content=""', f'content="{BASE_PATH}"')
    for prefix in ('href="/', 'src="/', 'action="/'):
        html = html.replace(prefix, prefix + BASE_PATH.lstrip("/" ) + "/")
    return html


def main():
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    shutil.copytree(ROOT / "static", OUTPUT / "static")
    for unwanted in OUTPUT.rglob(".DS_Store"):
        unwanted.unlink()

    with app.test_client() as client:
        for path in routes():
            response = client.get(path)
            if response.status_code >= 400:
                raise RuntimeError(f"Failed to render {path}: HTTP {response.status_code}")
            target = static_path(path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(rewrite_paths(response.get_data(as_text=True)), encoding="utf-8")

    (OUTPUT / ".nojekyll").touch()
    print(f"Built {len(routes())} pages in {OUTPUT}")


if __name__ == "__main__":
    main()
