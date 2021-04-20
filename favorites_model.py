class FavoritesModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS favorites 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(50),
                             word VARCHAR(50),
                             text VARCHAR(128)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, word, text):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO favorites 
                          (user_name, word, text) 
                          VALUES (?,?,?)''', (user_name, word, text,))
        cursor.close()
        self.connection.commit()

    def get(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM favorites WHERE id = ?", (str(id),))
        row = cursor.fetchone()
        return row

    def get_users(self, user_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM favorites WHERE user_name = ?", (user_name,))
        row = cursor.fetchall()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM favorites")
        rows = cursor.fetchall()
        return rows

    def delete(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM favorites WHERE id = {}'''.format((str(id))))
        cursor.close()
        self.connection.commit()

    def exists(self, word):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM favorites WHERE word = ? ", (word,))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)
