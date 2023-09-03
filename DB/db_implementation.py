from pathlib import Path
from os import path
import sqlite3

NAME_DB = 'sqlite3.db'
TABLE_NAME = 'activity'
BASE_DIR = Path(__file__).resolve().parent.parent
PATH_DB = path.join(BASE_DIR,NAME_DB)


class Activity_DB:
    def __init__(self):
        self.db = None

    def create_field(self, activity: dict):
        cursor = self.db.cursor()

        cursor.execute(f"""INSERT INTO {TABLE_NAME} (activity,type,participants,price,link,key,accessibility)
                        VALUES ("{activity['activity']}","{activity['type']}",{activity['participants']},{activity['price']},
                                "{activity['link']}","{activity['key']}",{activity['accessibility']})
        """)

        self.db.commit()

    def get_latest_entries(self, quantity=5):
        cursor = self.db.cursor()

        cursor.execute(f"""SELECT activity,type,participants,price,link,key,accessibility FROM {TABLE_NAME} 
                           ORDER BY id DESC
                           LIMIT {quantity}""")

        name_columns = [name[0] for name in cursor.description]
        latest_fields = []

        for filed in cursor.fetchall():
            filed_str = ''

            for idx,name in enumerate(name_columns):
                filed_str += f'{name} -> {filed[idx]}, '

            filed_str = filed_str[:-2]
            latest_fields.append(filed_str)

        return '\n'.join(latest_fields[::-1])


    def close(self):
        self.db.close()

    def connect(self):
        self.db = sqlite3.connect(PATH_DB)
        return self

    def _create_table(self):
        cursor = self.db.cursor()
        cursor.execute(f"""CREATE TABLE {TABLE_NAME} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        activity VARCHAR(255),  
                        type VARCHAR(255),
                        participants NUMERIC,
                        price NUMERIC,
                        link TEXT,
                        key STRING,
                        accessibility NUMERIC
                        )""")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()


def check_table_exist():
    with Activity_DB() as my_db:
        cursor = my_db.db.cursor()

        try:
            cursor.execute(f'SELECT * FROM {TABLE_NAME}')
        except sqlite3.OperationalError:
            my_db._create_table()


check_table_exist()
