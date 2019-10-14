from contextlib import closing
import sqlite3
create_teacher = """
CREATE TABLE IF NOT EXISTS teacher (
    id_teacher INTEGER PRIMARY KEY,
    nome VARCHAR(100)
); """

create_student = """
CREATE TABLE IF NOT EXISTS student (
    id_student INTEGER PRIMARY KEY,
    nome VARCHAR(100)
);
"""

create_subject = """
CREATE TABLE IF NOT EXISTS subject (
    id_subject INTEGER PRIMARY KEY,
    nome VARCHAR(100),
    status INTEGER,
    plano_ensino VARCHAR(200),
    carga_horaria INTEGER,
    id_coordenador INTEGER NOT NULL
        CONSTRAINT teacher REFERENCES teacher (id_teacher)
);
"""

def connect_database():
    return sqlite3.connect("database.db")

def create_database():
    with closing(connect_database()) as con, closing(con.cursor()) as cursor:
        cursor.execute(create_student)
        cursor.execute(create_teacher)
        cursor.execute(create_subject)

        con.commit()


def database_clear():
    with closing(connect_database()) as con, closing(con.cursor()) as cursor:
        cursor.execute('DELETE FROM student;')
        cursor.execute('DELETE FROM teacher;')
        cursor.execute('DELETE FROM subject;')

        con.commit()


def execute(sql, values = None):
    with closing(connect_database()) as con, closing(con.cursor()) as cursor:
        if values != None:
            cursor.execute(sql, values)
        else:
            cursor.execute(sql)
        
        con.commit()

def consult(sql: str, values = None):
    with closing(connect_database()) as con, closing(con.cursor()) as cursor:
        if values != None:
            cursor.execute(sql, values)
        else:
            cursor.execute(sql)

        result = cursor.fetchall()
        if result == None:
            return False

        return result


def register(sql: str, values = None):
    with closing(connect_database()) as con, closing(con.cursor()) as cursor:
        if values:
            cursor.execute(sql, values)
        else:
            cursor.execute(sql)

        con.commit()
        return cursor.lastrowid
