from pathlib import Path
import random
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from db import get_conn
from helpers import generate_engagement_suggestions

app = Flask(__name__)
BASE_DIR = Path(__file__).parent
PLATFORMS = ("x", "facebook", "linkedin")

@app.template_filter('uppercase')
def uppercase_filter(s):
    return s.upper() if s else ''

@app.route("/")
def index():
    category = request.args.get("category", "All")
    origin = request.args.get("origin", "All")
    page = int(request.args.get("page", 1))
    per_page = 10
    offset = (page - 1) * per_page

    conn = get_conn()
    cursor = conn.cursor()

    query = """
        SELECT a.id, a.title, a.url, a.published_at, a.fetched_at, a.summary, a.category, a.origin, s.name as source_name
        FROM articles a
        JOIN sources s ON a.source_id = s.id
        WHERE a.status = 'new'
    """
    params = []

    if category != "All":
        query += " AND a.category = ?"
        params.append(category)
    if origin != "All":
        query += " AND a.origin = ?"
        params.append(origin)

    # Count total items for pagination
    count_query = f"SELECT COUNT(*) FROM ({query})"
    cursor.execute(count_query, params)
    total_articles = cursor.fetchone()[0]
    total_pages = (total_articles + per_page - 1) // per_page or 1

    query += " ORDER BY a.fetched_at DESC, a.id DESC LIMIT ? OFFSET ?"
    params.extend([per_page, offset])

    cursor.execute(query, params)
    articles = cursor.fetchall()

    # Get Daily Quote
    cursor.execute("SELECT quote, author FROM quotes ORDER BY RANDOM() LIMIT 1")
    quote_row = cursor.fetchone()
    conn.close()

    return render_template(
        "index.html",
        articles=articles,
        category=category,
        origin=origin,
        page=page,
        total_pages=total_pages,
        total_articles=total_articles,
        quote=quote_row
    )

@app.route("/article/<int:article_id>")
def article(article_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, a.title, a.url, a.published_at, a.fetched_at, a.summary, a.category, a.origin, s.name as source_name
        FROM articles a
        JOIN sources s ON a.source_id = s.id
        WHERE a.id = ?
    """, (article_id,))
    art = cursor.fetchone()

    if not art:
        conn.close()
        abort(404)

    cursor.execute("SELECT platform, text FROM drafts WHERE article_id = ?", (article_id,))
    rows = cursor.fetchall()
    conn.close()

    suggestions = generate_engagement_suggestions(art["title"], art["summary"], art["category"])

    drafts = {p: "" for p in PLATFORMS}
    for row in rows:
        drafts[row["platform"]] = row["text"]

    # Pre-populate draft suggestions if empty
    if not drafts["linkedin"]:
        drafts["linkedin"] = suggestions["linkedin"]
    if not drafts["x"]:
        drafts["x"] = suggestions["x"]

    return render_template(
        "article.html",
        article=art,
        drafts=drafts,
        suggestions=suggestions,
        platforms=PLATFORMS
    )

@app.route("/mark/<int:article_id>/<status>")
def mark_status(article_id, status):
    if status not in ("selected", "rejected", "posted"):
        abort(400)
    conn = get_conn()
    with conn:
        conn.execute("UPDATE articles SET status = ? WHERE id = ?", (status, article_id))
    conn.close()
    return redirect(url_for("index"))

@app.route("/save_draft/<int:article_id>/<platform>", methods=["POST"])
def save_draft(article_id, platform):
    if platform not in PLATFORMS:
        abort(400)
    text = request.form.get("text", "")
    conn = get_conn()
    with conn:
        conn.execute("""
            INSERT INTO drafts (article_id, platform, text)
            VALUES (?, ?, ?)
            ON CONFLICT(article_id, platform) DO UPDATE SET text = excluded.text
        """, (article_id, platform, text))
    conn.close()
    return redirect(url_for("article", article_id=article_id))

@app.route("/posted/<int:article_id>", methods=["POST"])
def mark_posted(article_id):
    conn = get_conn()
    with conn:
        conn.execute("UPDATE articles SET status = 'posted' WHERE id = ?", (article_id,))
    conn.close()
    return redirect(url_for("index"))

@app.route("/manifest.json")
def manifest():
    return send_from_directory(BASE_DIR / "static", "manifest.json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
