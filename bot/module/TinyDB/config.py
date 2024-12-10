from tinydb import TinyDB, Query
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
DB_PATH = os.path.join(BASE_DIR, 'data', 'db.json')
QR_DIR = os.path.join(BASE_DIR, 'data', 'QR')

db = TinyDB(DB_PATH)

db_users = db.table('users')
