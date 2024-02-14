import sqlite3
from datetime import datetime
from config import DATABASE_PATH


class DBManager:
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.cursor.execute("PRAGMA journal_mode=WAL;")

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
                gpt3_free_tokens_update_date TEXT,
                mj52_limit INTEGER,
                mj6_limit INTEGER,
                gpt4_limit INTEGER,
                gpt35_limit INTEGER,
                temp_subscription TEXT
            )
            '''
            conn.execute(query)

    def create_context_table(self, name):
        with sqlite3.connect(self.db_path) as conn:
            query = f'''
            CREATE TABLE IF NOT EXISTS {name} (
                    id INTEGER PRIMARY KEY,
                    message TEXT,
                    role TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_id   INTEGER)'''
            conn.execute(query)

    def clear_context_table(self, name):
        """Очищает все данные из указанной таблицы контекста."""
        with sqlite3.connect(self.db_path) as conn:
            query = f"DELETE FROM {name}"
            conn.execute(query)
            conn.commit()

    def format_date(self, date_str):
        if date_str is None:
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

    def add_user(self, nickname, user_id, gpt_subscription_type, mj_subscription_type,
                 cur_gpt_mode, cur_mj_mode,
                 gpt3_tokens, mj52_limit,
                 mj6_limit, gpt4_limit, gpt35_limit, gpt3_free_tokens_update_date):
        # gpt_sub_update_date = self.format_date(gpt_sub_update_date)
        # mj_sub_update_date = self.format_date(mj_sub_update_date)
        # mj_daily_update_date = self.format_date(mj_daily_update_date)
        # gpt_daily_update_date = self.format_date(gpt_daily_update_date)
        gpt3_free_tokens_update_date = self.format_date(gpt3_free_tokens_update_date)

        with sqlite3.connect(self.db_path) as conn:
            query = '''INSERT INTO user (nickname, user_id, gpt_subscription_type, mj_subscription_type, 
                                        cur_gpt_mode, cur_mj_mode, 
                                        gpt3_tokens, mj52_limit, 
                                        mj6_limit, gpt4_limit, gpt35_limit, gpt3_free_tokens_update_date) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            conn.execute(query, (nickname, user_id, gpt_subscription_type, mj_subscription_type,
                                 cur_gpt_mode, cur_mj_mode,
                                 gpt3_tokens, mj52_limit,
                                 mj6_limit, gpt4_limit, gpt35_limit, gpt3_free_tokens_update_date))

    def update_user(self, user_id, **kwargs):
        for key, value in kwargs.items():
            if 'date' in key:
                kwargs[key] = self.format_date(value)

        with sqlite3.connect(self.db_path) as conn:
            try:
                columns = ', '.join([f"{k} = ?" for k in kwargs])
                values = list(kwargs.values())
                values.append(user_id)
                query = f'UPDATE user SET {columns} WHERE user_id = ?'
                conn.execute(query, values)
            except Exception as e:
                print(kwargs, '\n', e)

    def get_user(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row  # Установите фабрику строк для возврата данных в виде словаря
            cursor = conn.execute("SELECT * FROM user WHERE user_id = ?", (user_id,))
            return cursor.fetchone()

    def get_context_table(self, name):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row  # Установите фабрику строк для возврата данных в виде словаря
            cursor = conn.execute(f"SELECT * FROM {name}")
            return cursor.fetchone()

    def delete_user(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            query = 'DELETE FROM user WHERE user_id = ?'
            conn.execute(query, (user_id,))

    def add_context(self, user_id, message, role, tablename):
        """Добавление сообщения в контекст пользователя."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO {tablename} (user_id, message, role) VALUES (?, ?, ?)",
                (user_id, message, role)
            )
            conn.commit()

    def get_context(self, tablename):
        """Получение всего контекста общения пользователя, упорядоченного по времени."""
        with sqlite3.connect(self.db_path) as conn:
            result = self.cursor.execute(
                f"SELECT role, message FROM {tablename} ORDER BY timestamp"
            ).fetchall()

            # Преобразование результата в список словарей
            context = [{"role": role, "content": message} for role, message in result]
            return context

    def get_all_users(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row  # Установите фабрику строк для возврата данных в виде словаря
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user")
            users = cursor.fetchall()
            return [dict(user) for user in users]
