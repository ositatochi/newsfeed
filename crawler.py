import feedparser
import requests
from bs4 import BeautifulSoup
from db import get_conn

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch_full_body(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            body_text = " ".join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 30])
            return body_text[:3000] # Cap at 3000 chars for clean context
    except Exception as e:
        print(f"Could not scrape body for {url}: {e}")
    return ""

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
            for entry in feed.entries[:10]:
                title = entry.get("title", "No Title")
                url = entry.get("link", "")
                published_at = entry.get("published", entry.get("updated", None))
                summary = entry.get("summary", entry.get("description", ""))

                if not url:
                    continue

                category = detect_category(title, summary) or source["category"]
                origin = source["origin"]
                
                # Scrape full body text
                body_text = fetch_full_body(url)
                words = len(body_text.split()) if body_text else len(summary.split())
                reading_time = max(1, round(words / 180))

                cursor.execute(
                    """
                    INSERT OR IGNORE INTO articles (source_id, title, url, published_at, summary, body_text, reading_time, category, origin)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (source["id"], title, url, published_at, summary, body_text, reading_time, category, origin)
                )
                if cursor.rowcount > 0:
                    new_count += 1
        except Exception as e:
            print(f"Error crawling {source['name']}: {e}")

    conn.commit()
    conn.close()
    print(f"Fetched {new_count} new articles with full body intel.")

if __name__ == "__main__":
    crawl()
