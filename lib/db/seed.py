from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def seed_data():
    Author.delete_all()
    Magazine.delete_all()
    Article.delete_all()

    a1 = Author.create("Alice")
    a2 = Author.create("Bob")
    a3 = Author.create("Charlie")

    m1 = Magazine.create("Tech Monthly", "Technology")
    m2 = Magazine.create("Health Today", "Health")
    m3 = Magazine.create("Nature Weekly", "Science")

    a1.add_article(m1, "Python Tips")
    a1.add_article(m2, "Healthy Coding")
    a2.add_article(m1, "AI Trends")
    a3.add_article(m1, "Quantum Computing")
    a3.add_article(m1, "More Quantum Stuff")
    a3.add_article(m1, "Quantum Finale")
