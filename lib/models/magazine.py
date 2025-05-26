from lib.db.connection import get_connection
from lib.models.article import Article
from lib.models.author import Author

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
        self.id = cur.lastrowid
        conn.commit()
        conn.close()

    def list_articles(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Article(row['title'], row['author_id'], row['magazine_id'], row['id']) for row in rows]

    def list_contributors(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
        """, (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Author(row['name'], row['id']) for row in rows]
