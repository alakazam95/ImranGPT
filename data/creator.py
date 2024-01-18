import sqlite3


subscription_type = 'Basic'  # Заполнительное значение
user_limit = 100             # Заполнительное значение
limit_update_date = '2023-01-01'  # Заполнительное значение


class dbCreator():
    def __init__(self, DATABASE_PATH="C:\\Users\\job_j\\Documents\\GitHub\\amed\\ImranGPT\\data\\mydatabase.db"):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()
        self.check_table_structure()

    def check_table_structure(self):
        with self.conn:
            self.cursor.execute("PRAGMA table_info(user)")
            return self.cursor.fetchall()

    def close_connection(self):
        """Закрытие соединения с базой данных."""
        self.conn.close()

    def add_user(self, user_id, subscription_type='basic', user_limit=100, limit_update_date='2024-01-01'):
        with self.conn:
            self.cursor.execute('INSERT INTO user (user_id, subscription_type, user_limit, limit_update_date) VALUES (?, ?, ?, ?)',
                                (user_id, subscription_type, user_limit, limit_update_date))

    def user_exists(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT * FROM `user` WHERE `user_id` = ?", (user_id,)).fetchall()
            print(result)

    def get_users(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM user")
        users = c.fetchall()
        return users

    def set_nickname(self, user_id, nickname):
        with self.conn:
            self.cursor.execute("UPDATE `user` SET `nickname` = ? WHERE `user_id` = ?", (nickname, user_id))

    def get_nickname(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT `nickname` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchone()
            return result[0] if result else None

    def set_time_sub(self, user_id, time_sub):
        with self.conn:
            self.cursor.execute("UPDATE `user` SET `time_sub` = ? WHERE `user_id` = ?", (time_sub, user_id))

    def get_time_sub(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT `time_sub` FROM `user` WHERE `user_id` = ?", (user_id,)).fetchone()
            return result[0] if result else None

    def set_signup(self, user_id, signup):
        with self.conn:
            self.cursor.execute("UPDATE `user` SET `signup` = ? WHERE `user_id` = ?", (signup, user_id))

    def get_signup(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT `signup` FROM `user` WHERE `user_id` = ?", (user_id,)).fetchall()
            signup = None  # Инициализация переменной signup
            for row in result:
                signup = str(row[0])
            return signup

    def set_subscription_type(self, user_id, subscription_type):
        with self.conn:
            self.cursor.execute("UPDATE `user` SET `subscription_type` = ? WHERE `user_id` = ?",
                                (subscription_type, user_id))

    def get_subscription_type(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT `subscription_type` FROM `user` WHERE `user_id` = ?",
                                         (user_id,)).fetchone()
            return result[0] if result else None

    def set_user_limit(self, user_id, user_limit):
        with self.conn:
            self.cursor.execute("UPDATE `user` SET `user_limit` = ? WHERE `user_id` = ?", (user_limit, user_id))

    def get_user_limit(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT `user_limit` FROM `user` WHERE `user_id` = ?", (user_id,)).fetchone()
            return result[0] if result else None

    def set_limit_update_date(self, user_id, limit_update_date):
        with self.conn:
            self.cursor.execute("UPDATE `user` SET `limit_update_date` = ? WHERE `user_id` = ?",
                                (limit_update_date, user_id))

    def get_limit_update_date(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT `limit_update_date` FROM `user` WHERE `user_id` = ?",
                                         (user_id,)).fetchone()
            return result[0] if result else None
