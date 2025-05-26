from lib.db.connection import get_connection
from lib.models.article import Article
from lib.models.magazine import Magazine

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
        conn.commit()
        return cls(cursor.lastrowid, name)

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        return cls(row['id'], row['name']) if row else None

    @classmethod
    def delete_all(cls):
        conn = get_connection()
        conn.execute("DELETE FROM authors")
        conn.commit()

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        return [Article(**row) for row in cursor.fetchall()]

    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT DISTINCT m.* FROM magazines m
        JOIN articles a ON m.id = a.magazine_id
        WHERE a.author_id = ?
        """, (self.id,))
        return [Magazine(**row) for row in cursor.fetchall()]

    def add_article(self, magazine, title):
        return Article.create(title, self.id, magazine.id)

    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT DISTINCT m.category FROM magazines m
        JOIN articles a ON a.magazine_id = m.id
        WHERE a.author_id = ?
        """, (self.id,))
        return [row['category'] for row in cursor.fetchall()]
