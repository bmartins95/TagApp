import os

from .sqlite import SqliteInterface as sql

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

    def getListsFromProject(self, projectId):
        query = f"SELECT name FROM lists WHERE projectId = {projectId};"
        result = sql.executeAndReadQuery(self.connection, query)
        return result
    
    def getListIdFromProject(self, name, projectId):
        query = f"""
            SELECT id FROM lists 
            WHERE projectId = {projectId} AND name = '{name}';
        """
        result = sql.executeAndReadQuery(self.connection, query)
        return result[0][0]
    
    def getListName(self, id):
        query = f"SELECT name FROM lists WHERE id = {id};"
        result = sql.executeAndReadQuery(self.connection, query)
        return result[0][0]
    
    def getLinesFromList(self, listId):
        query = f"""
            SELECT tag, type, signal, pid, version 
            FROM lines WHERE listId == {listId};
        """
        result = sql.executeAndReadQuery(self.connection, query)
        return result

    def getProjectName(self, projectId):
        query = f"SELECT name FROM projects WHERE id = {projectId}"
        result = sql.executeAndReadQuery(self.connection, query)
        return result[0][0]

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


if __name__ == '__main__':
    path = "./database/teste.db"
    server = Server(path)
    server.addProject("Projeto 1")
    server.addList("Lista 1", 1)
    server.addLine("AHH3DF", "Causa", "Analógico", "Pressão alta H", 1, 1)
    server.addLine("ASGG4", "Causa", "Digital", "Pressão baixa L", 2, 1)
    server.addLine("ADH33", "Causa", "Analógico", "Pressão alta H", 1, 1)
    server.addLine("AF5GG", "Causa", "Analógico", "Falha na válvula", 5, 1)
    server.addLine("AKJJ7", "Causa", "Digital", "Falha", 4, 1)
    server.addList("Lista 2", 1)
    server.addLine("ADA33", "Causa", "Analógico", "Pressão alta H", 3, 2)
    server.addLine("131DD", "Efeito", "Digital", "Redução da pressão", 3, 2)
    server.addLine("ADHH4", "Causa", "Analógico", "Pressão alta H", 3, 2)
    server.addLine("HUJU7", "Causa", "Analógico", "Falha na válvula", 3, 2)
    server.addLine("FFF44F", "Efeito", "Digital", "Falha", 3, 2)