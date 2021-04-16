import os

from .sqlite import SqliteInterface as sql

class Server():
    def __init__(self, path):
        self.connection = sql.createConnection(path)
        self.createProjectsTable()
        self.createListsTable()
        self.createLinesTable()

    def getTable(self, name):
        query = f"SELECT * FROM '{name}';"
        result = sql.executeAndReadQuery(self.connection, query)
        return result

    def getLinesFromList(self, listId):
        query = f"""
            SELECT tag, type, signal, pid, version 
            FROM lines WHERE list_id == {listId};
        """
        result = sql.executeAndReadQuery(self.connection, query)
        return result

    def addProject(self, name, description="NULL"):
        query = f"""
            INSERT INTO projects (name, description)
            VALUES ('{name}', {description});
        """
        sql.executeQuery(self.connection, query)

    def addList(self, name, projectId):
        query = f"""
            INSERT INTO lists (name, project_id)
            VALUES ('{name}', {projectId});
        """
        sql.executeQuery(self.connection, query)

    def addLine(self, tag, type, signal, pid, version, listId):
        query = f"""
            INSERT INTO lines (tag, type, signal, pid, version, list_id)
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        sql.executeQuery(self.connection, query)

    def createListsTable(self):
        query = """ 
            CREATE TABLE IF NOT EXISTS lists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                project_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(project_id) REFERENCES projects(id)
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
                list_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(list_id) REFERENCES lists(id)
            );
        """
        sql.executeQuery(self.connection, query)


if __name__ == '__main__':
    path = "./database/teste.db"
    server = Server(path)
    server.addProject("Project 1")
    server.addList("List 1", 1)
    server.addLine("AHH3DF", "Causa", "Analógico", "Pressão alta H", 1, 1)
    server.addLine("ASGG4", "Causa", "Digital", "Pressão baixa L", 2, 1)
    server.addLine("ADH33", "Causa", "Analógico", "Pressão alta H", 1, 1)
    server.addLine("AF5GG", "Causa", "Analógico", "Falha na válvula", 5, 1)
    server.addLine("AKJJ7", "Causa", "Digital", "Falha", 4, 1)
    server.addList("List 2", 1)
    server.addLine("AHH3DF", "Causa", "Analógico", "Pressão alta H", 1, 2)
    server.addLine("ASGG4", "Causa", "Digital", "Pressão baixa L", 2, 2)
    server.addLine("ADH33", "Causa", "Analógico", "Pressão alta H", 1, 2)
    server.addLine("AF5GG", "Causa", "Analógico", "Falha na válvula", 5, 2)
    server.addLine("AKJJ7", "Causa", "Digital", "Falha", 4, 2)
    
    myList = server.getLinesFromList(1)
    
    for line in myList:
        print(line)

    print(len(myList))
    print(len(myList[0]) + 1)