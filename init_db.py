from db import get_conn

SCHEMA = """
CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    feed_url TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL DEFAULT 'Tech News',
    origin TEXT NOT NULL DEFAULT 'Global / US',
    active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    published_at TEXT,
    summary TEXT,
    category TEXT DEFAULT 'Tech News',
    origin TEXT DEFAULT 'Global / US',
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

CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT NOT NULL,
    author TEXT NOT NULL
);
"""

SEED_SOURCES = [
    ("TechCrunch", "https://techcrunch.com/feed/", "Tech News", "Global / US"),
    ("The Verge", "https://www.theverge.com/rss/index.xml", "Tech News", "Global / US"),
    ("Hacker News", "https://news.ycombinator.com/rss", "Software & Dev", "Global / US"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index", "Cybersecurity & Hacks", "Global / US"),
    ("MIT Tech Review", "https://www.technologyreview.com/feed/", "AI & ML", "Global / US"),
    ("TechCabal", "https://techcabal.com/feed/", "Tech News", "Nigeria / Africa")
]

SEED_QUOTES = [
    ("Simplicity is prerequisite for reliability.", "Edser W. Dijkstra"),
    ("Any sufficiently advanced technology is indistinguishable from magic.", "Arthur C. Clarke"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Artificial Intelligence is the new electricity.", "Andrew Ng"),
    ("The best way to predict the future is to invent it.", "Alan Kay")
]

def main():
    conn = get_conn()
    with conn:
        conn.executescript(SCHEMA)
        for name, url, cat, origin in SEED_SOURCES:
            conn.execute(
                "INSERT OR IGNORE INTO sources (name, feed_url, category, origin) VALUES (?, ?, ?, ?)",
                (name, url, cat, origin)
            )
        for q, a in SEED_QUOTES:
            conn.execute("INSERT OR IGNORE INTO quotes (quote, author) VALUES (?, ?)", (q, a))
    conn.close()

if __name__ == "__main__":
    main()
