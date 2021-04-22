import os

from server.sqlite import SqliteInterface as sql


class Server():
    def __init__(self, path="./server/database/teste.db"):
        self.connection = sql.createConnection(path)
        
        self.createProjectsTable()
        self.createListsTable()
        self.createLinesTable()

    def getTable(self, name):
        query = f"SELECT * FROM '{name}';"
        result = sql.executeAndReadQuery(self.connection, query)
        return result

    def getTableHeaders(self, name):
        query = f"SELECT * FROM '{name}';"
        result = sql.executeAndGetHeaders(self.connection, query)
        return result

    def getListsNameFromProject(self, projectId):
        query = f"SELECT name FROM lists WHERE projectId = {projectId};"
        result = sql.executeAndReadQuery(self.connection, query)
        return result
    
    def getListIdFromProject(self, name, projectId):
        query = f"""
            SELECT id FROM lists 
            WHERE projectId = {projectId} AND name = '{name}';
        """
        result = sql.executeAndReadQuery(self.connection, query)
        
        if not result:   
            return -1
        else:
            return result[0][0]
    
    def getListName(self, id):
        query = f"SELECT name FROM lists WHERE id = {id};"
        result = sql.executeAndReadQuery(self.connection, query)
        return result[0][0]
    
    def getLinesFromList(self, listId):
        query = f"""
            SELECT id, tag, type, signal, pid, version 
            FROM lines WHERE listId == {listId};
        """
        result = sql.executeAndReadQuery(self.connection, query)
        return result

    def getProjectName(self, projectId):
        query = f"SELECT name FROM projects WHERE id = {projectId}"
        result = sql.executeAndReadQuery(self.connection, query)
        return result[0][0]

    def updateLine(self, column, value, lineId):
        value = f"'{value}'" if type(value) == str else value
        query = f"""
        UPDATE lines
        SET {column} = {value}
        WHERE id = {lineId};
        """
        sql.executeQuery(self.connection, query)

    def addProject(self, name, description="NULL"):
        query = f"""
            INSERT INTO projects (name, description)
            VALUES ('{name}', '{description}');
        """
        sql.executeQuery(self.connection, query)

    def addList(self, name, projectId):
        query = f"""
            INSERT INTO lists (name, projectId)
            VALUES ('{name}', {projectId});
        """
        sql.executeQuery(self.connection, query)

    def addLine(self, tag, type, signal, pid, version, listId):
        query = f"""
            INSERT INTO lines (tag, type, signal, pid, version, listId)
            VALUES ('{tag}', '{type}', '{signal}', 
            '{pid}', {version}, {listId});
        """
        return sql.executeQuery(self.connection, query)

    def createProjectsTable(self):
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
