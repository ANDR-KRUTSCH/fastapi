from pathlib import Path
from sqlite3 import Cursor, connect


cursor: Cursor = None

class DataBaseManager:

    def __init__(self, DB_NAME: str | None = None) -> None:
        BASE_DIR = Path(__file__).resolve().parent.parent
        DB_DIR = BASE_DIR / 'db'

        if DB_NAME is None: self.DB_NAME = 'cryptid.db'
        else: self.DB_NAME = DB_NAME + '.db'

        self.DB_PATH = DB_DIR / self.DB_NAME

    @property
    def cursor(self) -> Cursor:
        global cursor
        if cursor is None: cursor = connect(database=self.DB_PATH, check_same_thread=False).cursor()
        return cursor


db_manager = DataBaseManager()
test_db_manager = DataBaseManager(DB_NAME='test')