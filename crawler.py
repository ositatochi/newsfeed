import feedparser
from db import get_conn

def detect_category(title, summary):
    text = f"{title} {summary}".lower()
    if any(k in text for k in ['ai', 'llm', 'gpt', 'neural', 'machine learning', 'claude', 'openai', 'gemini']):
        return "AI & ML"
    elif any(k in text for k in ['code', 'python', 'developer', 'software', 'git', 'api', 'bug', 'framework']):
        return "Software & Dev"
    elif any(k in text for k in ['hack', 'security', 'breach', 'vulnerability', 'phishing', 'malware', 'cyber']):
        return "Cybersecurity & Hacks"
    return "Tech News"

def crawl():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, feed_url, category, origin FROM sources WHERE active = 1")
    sources = cursor.fetchall()
    new_count = 0

    for source in sources:
        try:
            feed = feedparser.parse(source["feed_url"])
            for entry in feed.entries[:15]:
                title = entry.get("title", "No Title")
                url = entry.get("link", "")
                published_at = entry.get("published", entry.get("updated", None))
                summary = entry.get("summary", entry.get("description", ""))

                if not url:
                    continue

                category = detect_category(title, summary) or source["category"]
                origin = source["origin"]

                cursor.execute(
                    """
                    INSERT OR IGNORE INTO articles (source_id, title, url, published_at, summary, category, origin)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (source["id"], title, url, published_at, summary, category, origin)
                )
                if cursor.rowcount > 0:
                    new_count += 1
        except Exception as e:
            print(f"Error crawling {source['name']}: {e}")

    conn.commit()
    conn.close()
    print(f"Fetched {new_count} new articles.")

if __name__ == "__main__":
    crawl()
