from lib.models.author import Author
from lib.models.magazine import Magazine


alice = Author.find_by_name("Alice")
print("Alice's Articles:", alice.articles())
print("Alice's Magazines:", alice.magazines())

tech = Magazine.find_by_name("Tech Weekly")
print("Tech Weekly Contributors:", tech.contributors())
print("Tech Weekly Article Titles:", tech.article_titles())
