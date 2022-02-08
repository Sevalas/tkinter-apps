from sqlite3.dbapi2 import connect
from os.path import exists as pathexist
from os import makedirs
from task import Task

if not pathexist('./tm-database'):
    makedirs('./tm-database')

sqliteConn = connect('./tm-database/tasks.db')

cursor = sqliteConn.cursor()

def startDb():
    cursor.execute(
        """
            CREATE TABLE if not exists task (
                id INTEGER PRIMARY KEY,
                created_at TIMESTAMT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                description TEST NOT NULL,
                completed INTEGER NOT NULL
            );
        """
    )
    sqliteConn.commit()

def selectTasks():
    cursor.execute("SELECT id, created_at, description, completed from task")
    rows = cursor.fetchall()
    tasks: list(Task) = []
    for row in rows:
        task = Task(
            id=row[0],
            created_at=row[1],
            description=row[2],
            status=row[3]
            )
        tasks.append(task)
    return tasks

def insertTask(description):
    cursor.execute("INSERT INTO task (description, completed) VALUES (?, ?);", (description, 0))
    sqliteConn.commit()

def updateStatus(taskId, status):
    cursor.execute("UPDATE task SET completed = ? WHERE id = ?", (status, taskId))
    sqliteConn.commit()

def deleteTask(taskId):
    cursor.execute("DELETE FROM task WHERE id = ?", (taskId, ))
    sqliteConn.commit()