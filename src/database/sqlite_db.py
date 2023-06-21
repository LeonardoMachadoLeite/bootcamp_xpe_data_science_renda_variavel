import sqlite3
import os
import sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH")

class DatabaseConnectionFactory():
    def CreateDbConnection():
        return sqlite3.connect(SQLITE_DB_PATH, timeout=10)
    
