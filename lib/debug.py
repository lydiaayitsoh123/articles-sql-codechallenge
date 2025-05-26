from lib.db.connection import get_connection
from lib.db.seed import seed_data
seed_data()

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

import ipdb; ipdb.set_trace()
