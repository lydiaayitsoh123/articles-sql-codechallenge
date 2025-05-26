from lib.db.connection import get_connection
from lib.models.article import Article
from lib.models.magazine import Magazine

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def save_to_db(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
        self.id = cur.lastrowid
        conn.commit()
        conn.close()

    def write_article(self, magazine, title):
        article = Article(title, self.id, magazine.id)
        article.insert()
        return article

    def get_articles(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Article(row['title'], row['author_id'], row['magazine_id'], row['id']) for row in rows]

    def get_magazines(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Magazine(row['name'], row['category'], row['id']) for row in rows]
