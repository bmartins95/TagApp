from server.server import Server

if __name__ == '__main__':
    path = "./server/database/teste.db"
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