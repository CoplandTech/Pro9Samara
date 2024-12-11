from tinydb import TinyDB, Query
import os

from config import BASE_DIR

DB_PATH = os.path.join(BASE_DIR, 'data', 'db.json')

db = TinyDB(DB_PATH)

db_users = db.table('users')
