"""
Personal Portfolio: Flask backend
-----------------------------------
Routes:
  /                 home page (hero + featured projects)
  /about            about page
  /projects         all projects, with server-side search (?q=)
  /projects/<slug>  single project detail + screenshot lightbox
  /blog             blog index (posts loaded from content/blog/*.md)
  /blog/<slug>      single blog post, rendered from Markdown
  /contact          contact form (GET shows form, POST saves the message)
  /api/search       JSON search endpoint used by the live search box

Run with:  python3 app.py
Then open  http://127.0.0.1:5000
"""

import json
import os
import re
from datetime import datetime

import markdown
from flask import Flask, render_template, request, jsonify, abort

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, "content")
BLOG_DIR = os.path.join(CONTENT_DIR, "blog")
PROJECTS_FILE = os.path.join(CONTENT_DIR, "projects.json")
MESSAGES_FILE = os.path.join(CONTENT_DIR, "messages.json")

app = Flask(__name__)


def load_projects():
    with open(PROJECTS_FILE, encoding="utf-8") as f:
        return json.load(f)


def get_project(slug):
    for p in load_projects():
        if p["slug"] == slug:
            return p
    return None


def load_posts():
    """Read every .md file in content/blog, parse a tiny frontmatter block
    (title / date / tags as `key: value` lines followed by a blank line),
    and render the rest as HTML. This is the 'Markdown CMS': add a new
    .md file to content/blog and it appears on the site automatically."""
    posts = []
    if not os.path.isdir(BLOG_DIR):
        return posts

    for filename in os.listdir(BLOG_DIR):
        if not filename.endswith(".md"):
            continue
        path = os.path.join(BLOG_DIR, filename)
        with open(path, encoding="utf-8") as f:
            raw = f.read()

        meta, body = {}, raw
        if "\n\n" in raw:
            head, rest = raw.split("\n\n", 1)
            if all(":" in line for line in head.splitlines() if line.strip()):
                for line in head.splitlines():
                    key, _, value = line.partition(":")
                    meta[key.strip().lower()] = value.strip()
                body = rest

        slug = os.path.splitext(filename)[0]
        html = markdown.markdown(body, extensions=["fenced_code", "tables"])
        excerpt = re.sub("<[^<]+?>", "", body).strip().split("\n")[0][:180]

        posts.append({
            "slug": slug,
            "title": meta.get("title", slug.replace("-", " ").title()),
            "date": meta.get("date", ""),
            "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
            "html": html,
            "excerpt": excerpt,
        })

    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def get_post(slug):
    for p in load_posts():
        if p["slug"] == slug:
            return p
    return None

@app.route("/")
def home():
    projects = load_projects()[:3]
    return render_template("index.html", projects=projects, active="home")


@app.route("/about")
def about():
    return render_template("about.html", active="about")


@app.route("/projects")
def projects():
    q = request.args.get("q", "").strip().lower()
    all_projects = load_projects()
    if q:
        results = [p for p in all_projects if _project_matches(p, q)]
    else:
        results = all_projects
    return render_template(
        "projects.html",
        projects=results,
        all_projects_json=json.dumps(all_projects),
        query=q,
        active="projects",
    )


@app.route("/projects/<slug>")
def project_detail(slug):
    project = get_project(slug)
    if not project:
        abort(404)
    return render_template("project_detail.html", project=project, active="projects")


@app.route("/blog")
def blog():
    return render_template("blog.html", posts=load_posts(), active="blog")


@app.route("/blog/<slug>")
def blog_post(slug):
    post = get_post(slug)
    if not post:
        abort(404)
    return render_template("post.html", post=post, active="blog")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    sent = False
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            error = "Please fill in every field before sending."
        elif "@" not in email or "." not in email.split("@")[-1]:
            error = "That email address doesn't look right."
        else:
            _save_message(name, email, message)
            sent = True

    return render_template("contact.html", sent=sent, error=error, active="contact")

@app.route("/api/search")
def api_search():
    q = request.args.get("q", "").strip().lower()
    all_projects = load_projects()
    results = [p for p in all_projects if _project_matches(p, q)] if q else all_projects
    return jsonify(results)


def _project_matches(project, q):
    haystack = " ".join([
        project["title"],
        project["summary"],
        project["description"],
        " ".join(project["tags"]),
        " ".join(project["stack"]),
    ]).lower()
    return q in haystack


def _save_message(name, email, message):
    """Persist contact-form submissions to a local JSON file so the form
    works out of the box with no email server configured."""
    messages = []
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, encoding="utf-8") as f:
            try:
                messages = json.load(f)
            except json.JSONDecodeError:
                messages = []
    messages.append({
        "name": name,
        "email": email,
        "message": message,
        "received_at": datetime.now().isoformat(timespec="seconds"),
    })
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)


def send_email_notification(name, email, message):
    pass


if __name__ == "__main__":
    app.run(debug=True)
