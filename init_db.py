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
    body_text TEXT,
    reading_time INTEGER DEFAULT 1,
    category TEXT DEFAULT 'Tech News',
    origin TEXT DEFAULT 'Global / US',
    fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new','selected','rejected','posted')),
    FOREIGN KEY (source_id) REFERENCES sources (id)
);

CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT NOT NULL UNIQUE,
    author TEXT NOT NULL
);
"""

SEED_SOURCES = [
    ("TechCrunch Main", "https://techcrunch.com/feed/", "Tech News", "Global / US"),
    ("TechCrunch Hardware & Devices", "https://techcrunch.com/category/hardware/feed/", "Gadgets & Hardware", "Global / US"),
    ("TechCrunch Enterprise & AI", "https://techcrunch.com/category/enterprise/feed/", "AI & ML", "Global / US"),
    ("The Verge - Tech & Reviews", "https://www.theverge.com/rss/index.xml", "Gadgets & Hardware", "Global / US"),
    ("Hacker News", "https://news.ycombinator.com/rss", "Software & Dev", "Global / US"),
    ("Ars Technica - Security & Hacks", "https://feeds.arstechnica.com/arstechnica/index", "Cybersecurity & Hacks", "Global / US"),
    ("MIT Tech Review", "https://www.technologyreview.com/feed/", "AI & ML", "Global / US"),
    ("TechCabal", "https://techcabal.com/feed/", "Tech News", "Nigeria / Africa"),
    ("BleepingComputer - Hacks & Breaches", "https://www.bleepingcomputer.com/feed/", "Cybersecurity & Hacks", "Global / US"),
    ("Engadget - Gadgets & Launch", "https://www.engadget.com/rss.xml", "Gadgets & Hardware", "Global / US"),
    ("CNET Tech Reviews", "https://www.cnet.com/rss/news/", "Gadgets & Hardware", "Global / US"),
    ("TechNewsWorld", "https://www.technewsworld.com/feed/", "Software & Dev", "Global / US"),
    ("Mashable Tech", "https://mashable.com/feeds/rss/tech", "Tech News", "Global / US")
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
        conn.execute("DELETE FROM quotes WHERE id NOT IN (SELECT MIN(id) FROM quotes GROUP BY quote)")
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_quotes_quote_unique ON quotes (quote)")
        for name, url, cat, origin in SEED_SOURCES:
            conn.execute(
                """INSERT INTO sources (name, feed_url, category, origin) VALUES (?, ?, ?, ?)
                ON CONFLICT(feed_url) DO UPDATE SET
                    name = excluded.name,
                    category = excluded.category,
                    origin = excluded.origin""",
                (name, url, cat, origin)
            )
        for q, a in SEED_QUOTES:
            conn.execute("INSERT OR IGNORE INTO quotes (quote, author) VALUES (?, ?)", (q, a))
    conn.close()
    print("Database updated with device launch, hack, and review feeds.")

if __name__ == "__main__":
    main()
