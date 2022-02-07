import sqlite3


class sqliter:

    def __init__(self, db_file):    # Иницилизация БД
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def add_user(self, id):     # Добавление юзера в БД по его id
        if not self.user_exist('users', id):
            self.cursor.execute("INSERT INTO users (id) VALUES (?)", (id,))
            self.conn.commit()

    def user_exist(self, table, id):   # Проверка есть ли юзер в БД
        result = self.cursor.execute(f"SELECT id FROM {table} WHERE id = (?)", (id,))
        return bool(len(result.fetchall()))

    def get_user_info(self, id):       # Получение информации о юзере
        res = self.cursor.execute(f"SELECT * FROM records WHERE id = (?)", (id,)).fetchone()
        return {'id':res[0], 'notice':res[1], 'city':res[2], 'server_time':res[3], 'local_time':res[4]}

    def add_notice(self, id, city, server_time):     # Добавляет запись в records
        self.cursor.execute("INSERT INTO records (id, city, server_time) VALUES (?, ?, ?)", (id, city, server_time))
        self.conn.commit()

    def notice_update(self, id, arg):      # Принимает id и словарь
        self.cursor.execute(f"UPDATE records SET {arg[0]} = (?) WHERE id = (?)", (arg[1], id,))
        self.conn.commit()

    def tanimoto(self, s1, s2):
        a, b, c = len(s1), len(s2), 0.0
        for sym in s1:
            if sym in s2:
                c += 1
        return c / (a + b - c)

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    a = sqliter('database.db')