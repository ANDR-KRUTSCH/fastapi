from pathlib import Path
from sqlite3 import Cursor, connect


cursor: Cursor = None

def get_or_create_db(DB_NAME: str | None = None) -> tuple[Cursor, Path]:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_DIR = BASE_DIR / 'db'

    if DB_NAME is None: DB_NAME = 'cryptid.db'
    else: DB_NAME += '.db'

    DB_PATH = DB_DIR / DB_NAME

    global cursor
    if cursor is None or DB_NAME == 'test.db': cursor = connect(database=DB_PATH, check_same_thread=False).cursor()
    
    return cursor, DB_PATH