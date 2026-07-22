
موقع بورتفوليو شخصي فعليًا شغال: صفحات أساسية (الرئيسية/من أنا/المشاريع/تواصل)،
بحث حي في المشاريع، مدونة تُقرأ من ملفات Markdown (CMS بسيط)، نموذج تواصل يحفظ
الرسائل فعليًا، ومعرض صور بـ lightbox.

## Run it locally / تشغيل المشروع

```bash
cd portfolio
pip install -r requirements.txt
python3 app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## What's actually working

- **Search:** `/projects?q=python` works with JS off (server rendered) and
  with JS on (instant client-side filter backed by `/api/search`).
- **Contact form:** submits to Flask, validates fields, and saves each
  message to `content/messages.json`. To send real emails, fill in the
  `send_email_notification()` function in `app.py` with your SMTP details
  (instructions are in the code comments) and call it from the `/contact`
  route.
- **Blog / CMS:** drop a new `.md` file into `content/blog/` with a small
  header like:
  ```
  title: My New Post
  date: 2026-07-01
  tags: python, notes

  Body text starts after the blank line...
  ```
  and it appears on `/blog` automatically, with no database needed.
- **Projects:** edit `content/projects.json` to add or remove projects. Each
  project can have multiple screenshots (`images`), which open in a
  lightbox on the project detail page.

## Structure

```
app.py                  Flask routes (pages + search API + contact + blog)
templates/               Jinja2 HTML templates
static/css/style.css     All styling
static/js/main.js        Typing animation, search, lightbox, scroll reveal
content/projects.json    Project data
content/blog/*.md        Blog posts (Markdown CMS)
static/resume/resume.pdf Placeholder: replace with your real résumé
```


