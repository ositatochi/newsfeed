from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from db import get_conn
from helpers import generate_engagement_suggestions

app = Flask(__name__)
BASE_DIR = Path(__file__).parent

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

    # Total count for pagination
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

    conn.close()
    suggestions = generate_engagement_suggestions(art["title"], art["summary"], art["category"], art["origin"])

    return render_template("article.html", article=art, suggestions=suggestions)

@app.route("/mark/<int:article_id>/<status>")
def mark_status(article_id, status):
    if status not in ("selected", "rejected", "posted"):
        abort(400)
    conn = get_conn()
    with conn:
        conn.execute("UPDATE articles SET status = ? WHERE id = ?", (status, article_id))
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
