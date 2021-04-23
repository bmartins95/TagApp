import sqlite3


class SqliteInterface():
    """An interface with the sqlite3 package."""
    @staticmethod
    def createConnection(path: str):
        """Creates a connection with the server, if the request fail, the 
        function returns a error.
        """
        connection = None
        try:
            connection = sqlite3.connect(path)
        except sqlite3.Error as e:
            print(f"Error '{e}' occurred")

        return connection

    @staticmethod
    def executeQuery(connection, query: str):
        """Send a query to the server."""
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
        except sqlite3.Error as e:
            print(f"Error '{e}' occurred")

    @staticmethod
    def executeAndReadQuery(connection, query: str) -> list:
        """Send a query to the server and returns the answer."""
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Error '{e}' occurred")
    
    @staticmethod
    def executeAndGetHeaders(connection, query: str) -> tuple:
        """Send a query and return the query header, i.e. table columns names."""
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            headers =  [description[0] for description in cursor.description]
            return headers
        except sqlite3.Error as e:
            print(f"Error '{e}' occurred")
