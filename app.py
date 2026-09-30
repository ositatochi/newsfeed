import atexit
import math

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, abort, redirect, render_template, request, url_for

from crawler import crawl
from db import get_conn
from helpers import generate_engagement_suggestions

app = Flask(__name__)

# Keep crawling independently of incoming web requests.
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=crawl, trigger="interval", minutes=15, id="feed_crawl", max_instances=1)
scheduler.start()
atexit.register(lambda: scheduler.shutdown(wait=False) if scheduler.running else None)


@app.route("/")
def index():
    category = request.args.get("category", "All")
    origin = request.args.get("origin", "All")
    page = request.args.get("page", 1, type=int)
    per_page = 10

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT quote, author FROM quotes ORDER BY RANDOM() LIMIT 1")
    quote_row = cursor.fetchone()

    query = """
        SELECT a.id, a.title, a.url, a.published_at, a.fetched_at,
               a.category, a.origin, a.reading_time, s.name AS source_name
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

    cursor.execute(f"SELECT COUNT(*) FROM ({query})", params)
    total_articles = cursor.fetchone()[0]
    total_pages = max(1, math.ceil(total_articles / per_page))
    page = max(1, min(page, total_pages))
    offset = (page - 1) * per_page

    query += " ORDER BY a.id DESC LIMIT ? OFFSET ?"
    params.extend([per_page, offset])
    cursor.execute(query, params)
    articles = cursor.fetchall()
    conn.close()

    return render_template(
        "index.html",
        articles=articles,
        quote=quote_row,
        category=category,
        origin=origin,
        page=page,
        total_pages=total_pages,
        total_articles=total_articles,
    )


@app.route("/article/<int:article_id>")
def article(article_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT a.id, a.title, a.url, a.published_at, a.summary, a.body_text,
               a.reading_time, a.category, a.origin, s.name AS source_name
        FROM articles a
        JOIN sources s ON a.source_id = s.id
        WHERE a.id = ?
        """,
        (article_id,),
    )
    art = cursor.fetchone()
    conn.close()

    if not art:
        abort(404)

    suggestions = generate_engagement_suggestions(
        art["title"],
        art["summary"],
        art["body_text"],
        art["category"],
        art["origin"],
    )
    return render_template("article.html", article=art, suggestions=suggestions)


@app.route("/mark/<int:article_id>/<status>")
@app.route("/status/<int:article_id>/<status>")
def mark_status(article_id, status):
    if status not in ("selected", "rejected", "posted"):
        abort(400)

    conn = get_conn()
    with conn:
        conn.execute("UPDATE articles SET status = ? WHERE id = ?", (status, article_id))
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)