import sqlite3
import datetime
import config


class dbCreator():
    def __init__(self):
        self.conn = sqlite3.connect(config.DATABASE_PATH)
        self.cursor = self.conn.cursor()
        self.check_table_structure()

    def create_context_table(self, tablename):
        """Создание отдельной таблицы контекста для пользователя."""

        with self.conn:
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {tablename} (
                    id INTEGER PRIMARY KEY,
                    message TEXT,
                    role TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_id   INTEGER
                )
            """)

    def add_context(self, user_id, message, role, tablename):
        """Добавление сообщения в контекст пользователя."""

        with self.conn:
            self.cursor.execute(
                f"INSERT INTO {tablename} (user_id, message, role) VALUES (?, ?, ?)",
                (user_id, message, role)
            )

    def get_context(self, tablename):
        """Получение всего контекста общения пользователя, упорядоченного по времени."""
        with self.conn:
            result = self.cursor.execute(
                f"SELECT role, message FROM {tablename} ORDER BY timestamp"
            ).fetchall()

            # Преобразование результата в список словарей
            context = [{"role": role, "content": message} for role, message in result]
            return context

    def check_table_structure(self):
        with self.conn:
            self.cursor.execute("PRAGMA table_info(user)")
            return self.cursor.fetchall()

    def close_connection(self):
        """Закрытие соединения с базой данных."""
        self.conn.close()

    def add_user(self, user_id, nickname):
        with self.conn:
            self.cursor.execute(
                'INSERT INTO user (user_id, nickname) VALUES (?, ?)',
                (user_id, nickname))

    def user_exists(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT * FROM `user` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(result)

    def get_users(self):
        with self.conn:
            result = self.cursor.execute("SELECT * FROM user")
            users = result.fetchall()
            return users

    def set_nickname(self, user_id, nickname):
        with self.conn:
            self.cursor.execute("UPDATE `user` SET `nickname` = ? WHERE `user_id` = ?", (nickname, user_id))

    def get_nickname(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT `nickname` FROM `user` WHERE `user_id` = ?", (user_id,)).fetchone()
            return result[0] if result else None

    def set_subscription_type(self, user_id, subscription_type):
        with self.conn:
            self.cursor.execute("UPDATE `user` SET `subscription_type` = ? WHERE `user_id` = ?",
                                (subscription_type, user_id))

    def get_subscription_type(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT `subscription_type` FROM `user` WHERE `user_id` = ?",
                                         (user_id,)).fetchone()
            return result[0]

    def set_user_limit(self, user_id, user_limit):
        with self.conn:
            self.cursor.execute("UPDATE `user` SET `tokens_amount` = ? WHERE `user_id` = ?",
                                (user_limit, user_id))

    def get_user_limit(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT `tokens_amount` FROM `user` WHERE `user_id` = ?", (user_id,)).fetchone()
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

    def set_user_mode(self, user_id, selected_mode):
        with self.conn:
            self.cursor.execute("UPDATE `user` SET `user_mode` = ? WHERE `user_id` = ?",
                                (selected_mode, user_id))

    def get_user_mode(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT `user_mode` FROM `user` WHERE `user_id` = ?",
                                         (user_id,)).fetchone()
            return result[0] if result else "gpt-3.5-turbo"

    def update_tokens_amount(self, user_id, used_tokens):
        update_query = """
        UPDATE user
        SET tokens_amount = CASE
            WHEN tokens_amount > 0 AND tokens_amount - ? < 0 THEN 0
            WHEN tokens_amount > 0 THEN tokens_amount - ?
            ELSE tokens_amount - ?
        END
        WHERE user_id = ?
        """

        self.cursor.execute(update_query, (used_tokens, used_tokens, used_tokens, user_id))
        self.conn.commit()

    def check_tokens_limit(self, user_id):
        self.cursor.execute("SELECT tokens_amount FROM user WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        # Возвращает 0, если tokens_amount равно 0, иначе возвращает 1
        return 0 if result and result[0] == 0 else 1

    def delete_user_questions(self, tablename):
        """Удаление таблицы из базы данных по имени."""
        try:
            with self.conn:
                self.cursor.execute(f"DROP TABLE IF EXISTS {tablename}")
                print(f"Таблица {tablename} успешно удалена.")
        except sqlite3.Error as e:
            print(f"Ошибка при удалении таблицы {tablename}: {e}")

    def update_tokens_limit(self, user_id):
        update_query = """
        UPDATE user
        SET tokens_amount = CASE
            -- Если текущая дата и время >= limit_update_date и tokens_amount >= 0, устанавливаем tokens_amount в 50000
            WHEN datetime('now') >= datetime(limit_update_date) AND tokens_amount >= 0 THEN 50000
            -- Во всех остальных случаях оставляем tokens_amount без изменений
            ELSE tokens_amount
        END
        WHERE user_id = ?
        """

        self.cursor.execute(update_query, (user_id,))
        self.conn.commit()

        print('лимит обновлен')

    def get_gpt4_limit(self, user_id, user_limit):
        with self.conn:
            self.cursor.execute("UPDATE `user` SET `gpt-4_limit` = ? WHERE `user_id` = ?",
                                (user_limit, user_id))

    def set_gpt4_limit(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT `gpt-4_limit` FROM `user` WHERE `user_id` = ?",
                                         (user_id,)).fetchone()
            return result[0] if result else None
