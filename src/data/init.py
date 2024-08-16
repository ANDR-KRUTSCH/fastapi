import os
from pathlib import Path
from sqlite3 import connect, IntegrityError

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / 'db'

DB_NAME = os.environ.get('CRYPTID_SQLITE_DB')
if DB_NAME is None: DB_NAME = 'cryptid.db'
else: DB_NAME += '.db'

DB_PATH = DB_DIR / DB_NAME
    
connection = connect(database=DB_PATH, check_same_thread=False)
cursor = connection.cursor()