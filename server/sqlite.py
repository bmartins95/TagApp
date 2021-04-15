import sqlite3


class SqliteInterface():
    @staticmethod
    def createConnection(path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite database successful")
        except sqlite3.Error as e:
            print(f"Error '{e}' occurred")

        return connection

    @staticmethod
    def executeQuery(connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except sqlite3.Error as e:
            print(f"Error '{e}' occurred")

    @staticmethod
    def executeAndReadQuery(connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Error '{e}' occurred")
