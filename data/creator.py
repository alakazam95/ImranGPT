import sqlite3
from datetime import datetime
from config import DATABASE_PATH


class DBManager:
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            query = '''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT,
                user_id INTEGER UNIQUE,
                gpt_subscription_type TEXT,
                mj_subscription_type TEXT,
                gpt_sub_update_date TEXT,
                mj_sub_update_date TEXT,
                cur_gpt_mode TEXT,
                cur_mj_mode TEXT,
                gpt3_tokens INTEGER,
                mj_daily_update_date TEXT,
                gpt_daily_update_date TEXT,
                mj52_limit INTEGER,
                mj6_limit INTEGER,
                gpt4_limit INTEGER,
                gpt35_limit INTEGER
            )
            '''
            conn.execute(query)

    def format_date(self, date_str):
        if date_str is None:
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")


    def add_user(self, nickname, user_id, gpt_subscription_type, mj_subscription_type,
                 gpt_sub_update_date, mj_sub_update_date, cur_gpt_mode, cur_mj_mode,
                 gpt3_tokens, mj_daily_update_date, gpt_daily_update_date, mj52_limit,
                 mj6_limit, gpt4_limit, gpt35_limit):
        gpt_sub_update_date = self.format_date(gpt_sub_update_date)
        mj_sub_update_date = self.format_date(mj_sub_update_date)
        mj_daily_update_date = self.format_date(mj_daily_update_date)
        gpt_daily_update_date = self.format_date(gpt_daily_update_date)

        with sqlite3.connect(self.db_path) as conn:
            query = '''INSERT INTO user (nickname, user_id, gpt_subscription_type, mj_subscription_type, 
                                        gpt_sub_update_date, mj_sub_update_date, cur_gpt_mode, cur_mj_mode, 
                                        gpt3_tokens, mj_daily_update_date, gpt_daily_update_date, mj52_limit, 
                                        mj6_limit, gpt4_limit, gpt35_limit) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            conn.execute(query, (nickname, user_id, gpt_subscription_type, mj_subscription_type,
                                 gpt_sub_update_date, mj_sub_update_date, cur_gpt_mode, cur_mj_mode,
                                 gpt3_tokens, mj_daily_update_date, gpt_daily_update_date, mj52_limit,
                                 mj6_limit, gpt4_limit, gpt35_limit))

    def update_user(self, user_id, **kwargs):
        for key, value in kwargs.items():
            if 'date' in key:
                kwargs[key] = self.format_date(value)

        with sqlite3.connect(self.db_path) as conn:
            columns = ', '.join([f"{k} = ?" for k in kwargs])
            values = list(kwargs.values())
            values.append(user_id)
            query = f'UPDATE user SET {columns} WHERE user_id = ?'
            conn.execute(query, values)

    def get_user(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row  # Установите фабрику строк для возврата данных в виде словаря
            cursor = conn.execute("SELECT * FROM user WHERE user_id = ?", (user_id,))
            return cursor.fetchone()

    def delete_user(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            query = 'DELETE FROM user WHERE user_id = ?'
            conn.execute(query, (user_id,))

    def get_all_users(self):
        with sqlite3.connect(self.db_path) as conn:
            query = 'SELECT * FROM user'
            cursor = conn.execute(query)
            return cursor.fetchall()



