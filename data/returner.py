# import os
# import sqlite3
#
#
# class DBManager:
#     def __init__(self, db_filename):
#         self.db_filename = db_filename
#
#     def connect(self):
#         return sqlite3.connect(self.db_filename)
#
#     def create_table(self):
#         with self.connect() as conn:
#             c = conn.cursor()
#             c.execute('''CREATE TABLE IF NOT EXISTS users
#                         (id INTEGER PRIMARY KEY,
#                          subscription_type TEXT,
#                          user_limit INTEGER,
#                          limit_update_date TEXT)''')
#
#     def add_user(self, subscription_type, user_limit, limit_update_date):
#         with self.connect() as conn:
#             c = conn.cursor()
#             c.execute("INSERT INTO users (subscription_type, user_limit, limit_update_date) VALUES (?, ?, ?)",
#                       (subscription_type, user_limit, limit_update_date))
#
#     def get_all_users(self):
#         with self.connect() as conn:
#             c = conn.cursor()
#             c.execute("SELECT * FROM user")
#             return c.fetchall()
#
#     def get_user_id(self, user_id):
#         with self.connect() as conn:
#             c = conn.cursor()
#             c.execute("SELECT id FROM users WHERE id = ?", (user_id,))
#             return c.fetchone()
#
#     def get_subscription_type(self, user_id):
#         with self.connect() as conn:
#             c = conn.cursor()
#             c.execute("SELECT subscription_type FROM users WHERE id = ?", (user_id,))
#             return c.fetchone()
#
#     def get_user_limit(self, user_id):
#         with self.connect() as conn:
#             c = conn.cursor()
#             c.execute("SELECT user_limit FROM users WHERE id = ?", (user_id,))
#             return c.fetchone()
#
#     def get_limit_update_date(self, user_id):
#         with self.connect() as conn:
#             c = conn.cursor()
#             c.execute("SELECT limit_update_date FROM users WHERE id = ?", (user_id,))
#             return c.fetchone()
#
#     def show_tables(self):
#         with self.connect() as conn:
#             c = conn.cursor()
#             c.execute("SELECT name FROM sqlite_master WHERE type='table';")
#             tables = c.fetchall()
#             return tables
#
#
# DATABASE_PATH = 'C:\\Users\\job_j\\Documents\\GitHub\\amed\\ImranGPT\\data\\mydatabase.db'
# print(DATABASE_PATH)
# db_manager = DBManager(DATABASE_PATH)
# tables = db_manager.show_tables()
# for table in tables:
#     print(table[0])
#
# print(db_manager.get_all_users())
