import sqlite3
import json
from datetime import datetime
from config import DB_PATH

def init_db():
    """Initialize database with schema."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Posts table
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            platform TEXT NOT NULL,
            author TEXT,
            title TEXT,
            content TEXT,
            url TEXT,
            created_at TIMESTAMP,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source_metadata TEXT
        )
    ''')

    # Classifications table
    c.execute('''
        CREATE TABLE IF NOT EXISTS classifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id TEXT NOT NULL UNIQUE,
            threat_category TEXT,
            severity TEXT,
            confidence TEXT,
            reasoning TEXT,
            signals TEXT,
            human_verified INTEGER DEFAULT 0,
            verified_at TIMESTAMP,
            verified_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(id)
        )
    ''')

    # Signals table (extracted evidence)
    c.execute('''
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            classification_id INTEGER NOT NULL,
            signal_type TEXT,
            signal_text TEXT,
            confidence TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (classification_id) REFERENCES classifications(id)
        )
    ''')

    # Research brief table
    c.execute('''
        CREATE TABLE IF NOT EXISTS research_briefs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            summary TEXT,
            findings TEXT,
            methodology TEXT,
            limitations TEXT,
            recommendations TEXT,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def insert_post(post_id, platform, author, title, content, url, created_at, source_metadata=None):
    """Insert a post into database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        c.execute('''
            INSERT OR IGNORE INTO posts
            (id, platform, author, title, content, url, created_at, source_metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (post_id, platform, author, title, content, url, created_at,
              json.dumps(source_metadata) if source_metadata else None))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error inserting post: {e}")
        return False
    finally:
        conn.close()

def insert_classification(post_id, threat_category, severity, confidence, reasoning, signals):
    """Insert classification for a post."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        c.execute('''
            INSERT OR REPLACE INTO classifications
            (post_id, threat_category, severity, confidence, reasoning, signals)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (post_id, threat_category, severity, confidence, reasoning,
              json.dumps(signals) if signals else None))
        conn.commit()
        return c.lastrowid
    except Exception as e:
        print(f"Error inserting classification: {e}")
        return None
    finally:
        conn.close()

def get_unverified_high_confidence():
    """Fetch high-confidence, unverified classifications for review."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('''
        SELECT c.*, p.content, p.author, p.url, p.platform
        FROM classifications c
        JOIN posts p ON c.post_id = p.id
        WHERE c.human_verified = 0 AND c.confidence = 'high'
        ORDER BY c.created_at DESC
        LIMIT 20
    ''')

    results = c.fetchall()
    conn.close()
    return results

def get_statistics():
    """Get summary statistics."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    stats = {}

    # Total posts
    c.execute('SELECT COUNT(*) FROM posts')
    stats['total_posts'] = c.fetchone()[0]

    # Threat classification breakdown
    c.execute('''
        SELECT threat_category, COUNT(*) as count
        FROM classifications WHERE threat_category IS NOT NULL
        GROUP BY threat_category
    ''')
    stats['by_category'] = {row[0]: row[1] for row in c.fetchall()}

    # Severity breakdown
    c.execute('''
        SELECT severity, COUNT(*) as count
        FROM classifications WHERE severity IS NOT NULL
        GROUP BY severity
    ''')
    stats['by_severity'] = {row[0]: row[1] for row in c.fetchall()}

    # Confidence breakdown
    c.execute('''
        SELECT confidence, COUNT(*) as count
        FROM classifications WHERE confidence IS NOT NULL
        GROUP BY confidence
    ''')
    stats['by_confidence'] = {row[0]: row[1] for row in c.fetchall()}

    conn.close()
    return stats
