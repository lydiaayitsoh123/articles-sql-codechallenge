from lib.db.connection import get_connection
from lib.models.article import Article
from lib.models.author import Author

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    @classmethod
    def create(cls, name, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category))
        conn.commit()
        return cls(cursor.lastrowid, name, category)

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        return cls(row['id'], row['name'], row['category']) if row else None

    @classmethod
    def delete_all(cls):
        conn = get_connection()
        conn.execute("DELETE FROM magazines")
        conn.commit()

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        return [Article(**row) for row in cursor.fetchall()]

    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT DISTINCT a.* FROM authors a
        JOIN articles ar ON a.id = ar.author_id
        WHERE ar.magazine_id = ?
        """, (self.id,))
        return [Author(**row) for row in cursor.fetchall()]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        return [row['title'] for row in cursor.fetchall()]

    def contributing_authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT a.*, COUNT(ar.id) as article_count
        FROM authors a
        JOIN articles ar ON a.id = ar.author_id
        WHERE ar.magazine_id = ?
        GROUP BY a.id
        HAVING article_count > 2
        """, (self.id,))
        return [Author(**row) for row in cursor.fetchall()]
