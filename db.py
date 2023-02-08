import sqlite3

"Класс работающий с базой данных "
class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    '''Проверка наличия пользователя в базе'''
    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'users' WHERE user_id =? ",(user_id,)).fetchall()
            return  bool(len(result))

    '''Добавление пользователя в базу'''
    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))

    '''Изменение и установка логина пользователя'''
    def set_login_user(self,user_id,steam_login):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET steam_login = ? WHERE user_id = ?  ", (steam_login, user_id,))

    '''Возврат данных о логине пользователя'''
    def get_login_user(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT steam_login FROM 'users' WHERE user_id =? ", (user_id,)).fetchmany(1)
            return str(result[0][0])


    '''Добавление в базу выставленного счета на оплату'''
    def add_check(self, user_id, money, bill_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'check' ('user_id','money','bill_id') VALUES (?,?,?)", (user_id, money, bill_id,))

    '''Возврат данных счета выставленного пользователю'''
    def get_check(self, bill_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'check' WHERE bill_id =? ", (bill_id,)).fetchmany(1)
            if not bool(len(result)):
                    return False
            return result[0]

    '''Удаление счета из базы'''
    def delete_check(self, bill_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM 'check' WHERE bill_id = ?", (bill_id,))

    '''Сеттер состояния диалога'''
    def set_l(self,user_id,set):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET set_login = ? WHERE user_id = ?  ", (set,user_id,))

    '''Геттер состояния диалога'''
    def get_l(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT set_login FROM 'users' WHERE user_id =? ", (user_id,)).fetchmany(1)
            return bool(result[0][0])

    '''Сеттер состояния диалога'''
    def set_a(self,user_id,set):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET set_amount = ? WHERE user_id = ?  ", (set,user_id,))

    '''Геттер состояния диалога'''
    def get_a(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT set_amount FROM 'users' WHERE user_id =? ", (user_id,)).fetchmany(1)
            return bool(result[0][0])
