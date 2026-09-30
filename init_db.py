from db import get_conn

SCHEMA = """
CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    feed_url TEXT NOT NULL UNIQUE,
    active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    published_at TEXT,
    summary TEXT,
    fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new','selected','rejected','posted')),
    FOREIGN KEY (source_id) REFERENCES sources (id)
);

CREATE TABLE IF NOT EXISTS drafts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER NOT NULL,
    platform TEXT NOT NULL CHECK (platform IN ('x','facebook','linkedin')),
    text TEXT NOT NULL,
    posted_at DATETIME,
    UNIQUE(article_id, platform),
    FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE
);
"""

SEED_SOURCES = [
    ("TechCrunch", "https://techcrunch.com/feed/"),
    ("The Verge", "https://www.theverge.com/rss/index.xml"),
    ("Hacker News", "https://news.ycombinator.com/rss"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index")
]

def main():
    conn = get_conn()
    with conn:
        conn.executescript(SCHEMA)
        for name, url in SEED_SOURCES:
            conn.execute(
                "INSERT OR IGNORE INTO sources (name, feed_url) VALUES (?, ?)",
                (name, url)
            )
    conn.close()

if __name__ == "__main__":
    main()
