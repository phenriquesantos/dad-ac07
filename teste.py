from flask import Flask, request, jsonify
from contextlib import closing

import sqlite3

app = Flask(__name__)

sql_create = """
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50),
    telefone VARCHAR(11)
);
"""

def conectar():
    return sqlite3.connect("pessoa.db")

def criar_bd():
    with closing(conectar()) as conn, closing(conn.cursor()) as cursor:
        cursor.execute(sql_create)
        conn.commit()

def detalhar_usuario(id_usuario):
    sql = "SELECT nome, telefone FROM usuario WHERE id_usuario = ?"
    with closing(conectar()) as conn, closing(conn.cursor()) as cursor:
        cursor.execute(sql, (id_usuario, ))
        r = cursor.fetchone()
        if r == None: return None
        return {"nome": r[0], "telefone": r[1]}

def listar_usuarios():
    sql = "SELECT id_usuario, nome, telefone FROM usuario"
    with closing(conectar()) as conn, closing(conn.cursor()) as cursor:
        resultados = []
        cursor.execute(sql)
        linhas = cursor.fetchall()
        for id_usuario, nome, telefone in linhas:
            resultados.append({"id_usuario": id_usuario, "nome": nome, "telefone": telefone})
        return resultados

def cadastrar_usuario(nome, telefone):
    sql = "INSERT INTO usuario(nome, telefone) VALUES (?, ?)"
    with closing(conectar()) as conn, closing(conn.cursor()) as cursor:
        cursor.execute(sql, (nome, telefone))
        conn.commit()
        return cursor.lastrowid

@app.route("/pessoa")
def listar():
    lista = listar_usuarios()
    return jsonify(lista)

@app.route("/pessoa/<int:id_usuario>")
def detalhar(id_usuario):
    dic = detalhar_usuario(id_usuario)
    if dic == None: return "", 404
    return jsonify(dic)

@app.route("/pessoa", methods = ["POST"])
def cadastrar():
    dados = request.get_json()
    nome = dados['nome']
    telefone = dados['telefone']
    dic = {"id_usuario": cadastrar_usuario(nome, telefone)}
    return jsonify(dic)

criar_bd()

if __name__ == "__main__":
    app.run(port = 5000)