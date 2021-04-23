import os

from server.sqlite import SqliteInterface as sql


class Server():
    """Creates connections with the database, send queries and build the three 
    main tables, projects, lists and lines.
    """
    def __init__(self, path: str = "./server/database/teste.db"):
        self.connection = sql.createConnection(path)
        
        self.createProjectsTable()
        self.createListsTable()
        self.createLinesTable()

    def getTable(self, name: str):
        """Returns all data stored in the table."""
        query = f"SELECT * FROM '{name}';"
        result = sql.executeAndReadQuery(self.connection, query)
        return result

    def getTableHeaders(self, name: str) -> tuple:
        """Returns table headers."""
        query = f"SELECT * FROM '{name}';"
        result = sql.executeAndGetHeaders(self.connection, query)
        return result

    def getListsNameFromProject(self, projectId: int) -> list:
        """Returns name of lists for a given projectId."""
        query = f"SELECT name FROM lists WHERE projectId = {projectId};"
        result = sql.executeAndReadQuery(self.connection, query)
        return result
    
    def getListIdFromProject(self, name: str, projectId: int) -> int:
        """Returns the id of a list with the name in argument and that belongs
        to a project with projectId. If no list is found the function returns -1.
        """
        query = f"""
            SELECT id FROM lists 
            WHERE projectId = {projectId} AND name = '{name}';
        """
        result = sql.executeAndReadQuery(self.connection, query)
        
        if not result:   
            return -1
        else:
            return result[0][0]
    
    def getListName(self, id: int) -> str:
        """Search for a list by her id and returns her name."""
        query = f"SELECT name FROM lists WHERE id = {id};"
        result = sql.executeAndReadQuery(self.connection, query)
        return result[0][0]
    
    def getLinesFromList(self, listId: int) -> list:
        """Returns the columns id, tag, type, signal, pid, version for a given
        idList.
        """
        query = f"""
            SELECT id, tag, type, signal, pid, version 
            FROM lines WHERE listId == {listId};
        """
        result = sql.executeAndReadQuery(self.connection, query)
        return result

    def getProjectName(self, projectId: int) -> str:
        """Search for a project by his id and return his name."""
        query = f"SELECT name FROM projects WHERE id = {projectId}"
        result = sql.executeAndReadQuery(self.connection, query)
        return result[0][0]

    def updateLine(self, column: str, value: [str,int], lineId: int):
        """Updates a single value in the lines table, using the column name
        and line id as filters.
        """
        value = f"'{value}'" if type(value) == str else value
        query = f"""
        UPDATE lines
        SET {column} = {value}
        WHERE id = {lineId};
        """
        sql.executeQuery(self.connection, query)

    def addProject(self, name: str, description: str = "NULL"):
        """Adds a new project name to the project table."""
        query = f"""
            INSERT INTO projects (name, description)
            VALUES ('{name}', '{description}');
        """
        sql.executeQuery(self.connection, query)

    def addList(self, name: str, projectId: int):
        """Adds a new list to the lists table."""
        query = f"""
            INSERT INTO lists (name, projectId)
            VALUES ('{name}', {projectId});
        """
        sql.executeQuery(self.connection, query)

    def addLine(
        self, tag: str, type: str, signal: str, 
        pid: str, version: int, listId: str):
        """Adds a new line to the lines table."""
        query = f"""
            INSERT INTO lines (tag, type, signal, pid, version, listId)
            VALUES ('{tag}', '{type}', '{signal}', 
            '{pid}', {version}, {listId});
        """
        return sql.executeQuery(self.connection, query)

    def createProjectsTable(self):
        """Creates project table."""
        query = """ 
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        sql.executeQuery(self.connection, query)

    def createListsTable(self):
        """Creates lists table."""
        query = """ 
            CREATE TABLE IF NOT EXISTS lists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                projectId INTEGER NOT NULL,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(projectId) REFERENCES projects(id)
            );
        """
        sql.executeQuery(self.connection, query)


    def createLinesTable(self):
        """Creates lines table."""
        query = """ 
            CREATE TABLE IF NOT EXISTS lines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT,
                type TEXT,
                signal TEXT,
                pid TEXT,
                version INTEGER,
                listId INTEGER,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(listId) REFERENCES lists(id)
            );
        """
        sql.executeQuery(self.connection, query)
