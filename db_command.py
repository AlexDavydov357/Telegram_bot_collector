import sqlite3


class BotDB:

    # Подключение к базе
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем наличие юзера в базе"""
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем юзера из базы по его user_id"""
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        return self.conn.commit()

    def add_record(self, records, user_id, value):
        """Создаем запись"""
        self.cursor.execute(f"INSERT INTO {records} (user_id, path_to_file) VALUES (?, ?)",
                            (self.get_user_id(user_id), value))
        return self.conn.commit()

    def get_info(self):
        """Возвращает количество уникальных пользователей и их список, выводит информацию в терминал"""
        result = self.cursor.execute("SELECT * FROM users WHERE user_id = user_id")
        users = [item[1] for item in result.fetchall()]
        print(f"Количество уникальных пользователей {len(users)}")
        print(*users)
        return users

    def get_records(self, records, user_id, within='all'):
        """Получаем записи по пользователю
        day - за день
        week - за неделю
        month - за месяц
        по умолачанию, получаем все записи пользователя"""

        if within == "day":
            result = self.cursor.execute(f"SELECT * FROM {records} WHERE user_id = ? \
            AND date BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY date", \
                                         (self.get_user_id(user_id),))
        if within == "week":
            result = self.cursor.execute(f"SELECT * FROM {records} WHERE user_id = ? \
            AND date BETWEEN datetime('now', '- 6 days') AND datetime('now', 'localtime') ORDER BY date", \
                                         (self.get_user_id(user_id),))
        if within == "month":
            result = self.cursor.execute(f"SELECT * FROM {records} WHERE user_id = ? \
            AND date BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime') ORDER BY date", \
                                         (self.get_user_id(user_id),))
        else:
            result = self.cursor.execute(f"SELECT * FROM {records} WHERE user_id = ? ORDER BY date", \
                                         (self.get_user_id(user_id),))
        items = [item[2] for item in result.fetchall()]
        return items

    def close(self):
        """Закрываем соединение c БД"""
        self.conn.close()
