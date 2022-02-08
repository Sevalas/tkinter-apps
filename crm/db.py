from sqlite3.dbapi2 import connect
from client import Client
from os.path import exists as pathexist
from os import makedirs

if not pathexist('./crm-database'):
    makedirs('./crm-database')

sqliteConn = connect('./crm-database/crm.db')

cursor = sqliteConn.cursor()

def startDb():
    cursor.execute(
        """
            CREATE TABLE if not exists client (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                names TEXT NOT NULL,
                phone TEXT NOT NULL,
                enterprise TEXT NOT NULL,
                creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """
    )
    sqliteConn.commit()

def selectClients():
    cursor.execute("SELECT id, names, phone, enterprise, creation_date from client")
    rows = cursor.fetchall()
    clients: list(Client) = []
    for row in rows:
        client = Client(
            id = row[0],
            names = row[1],
            phone = row[2],
            enterprise = row[3],
            creation_date = row[4],
            )
        clients.append(client)
    return clients

def selectClientsbyId(clientsIdList):
    cursor.execute(
        "SELECT id, names, phone, enterprise, creation_date from client WHERE id in ({id_seq})".format(
            id_seq =','.join(['?']*len(clientsIdList))
        ),
        clientsIdList
    )
    rows = cursor.fetchall()
    clients: list(Client) = []
    for row in rows:
        client = Client(
            id = row[0],
            names = row[1],
            phone = row[2],
            enterprise = row[3],
            creation_date = row[4],
            )
        clients.append(client)
    return clients

def insertClient(client: Client):
    cursor.execute("INSERT INTO client (names, phone, enterprise) VALUES (?, ?, ?);", (client.names, client.phone, client.enterprise))
    sqliteConn.commit()

def updateClient(client: Client):
    cursor.execute("UPDATE client SET names = ?, phone = ?, enterprise = ? WHERE id = ?", (client.names, client.phone, client.enterprise, client.id))
    sqliteConn.commit()

def deleteClients(clientsIdList):
    
    cursor.execute(
        "DELETE FROM client WHERE id in ({id_seq})".format(
            id_seq =','.join(['?']*len(clientsIdList))
        ),
        clientsIdList
    )
    sqliteConn.commit()