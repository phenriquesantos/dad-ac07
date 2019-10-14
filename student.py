from flask import Blueprint, request, jsonify

import database

student_app = Blueprint('student_app', __name__)


def to_dic(rows: list) -> list:
    result = []
    for id, nome in rows:
        result.append({'id': id, 'nome': nome})

    return result


def consult_single_student(id: str):
    sql = "SELECT * FROM student WHERE id_student = ?"
    result = database.consult(sql, (id, ))
    if result:
        return to_dic(result)[0]


def consult_all_student():
    sql = "SELECT * FROM student"
    result = database.consult(sql, None)
    if result:
        return to_dic(result)

    return []


def delete_student(id):
    sql = "DELETE FROM student WHERE id_student = ?"
    database.execute(sql, (id, ))
    return True


def register_student(id, nome):
    sql = "INSERT INTO student(id_student, nome) VALUES (?, ?)"
    return database.register(sql, (id, nome))


def update_student(id, nome):
    sql = "UPDATE student SET nome = ? WHERE id_student = ?"
    database.execute(sql, (nome, id))
    return True


@student_app.route('/alunos')
def get_all_student():
    return jsonify(consult_all_student())


@student_app.route('/alunos', methods=["POST"])
def store_student():
    if 'nome' not in request.json.keys():
        return jsonify({'erro': 'aluno sem nome'}), 404

    new_student = request.json
    if consult_single_student(str(new_student['id'])):
        return jsonify({'erro': 'id já utilizada'}), 404

    register_student(new_student['id'], new_student['nome'])
    return {'success': True}, 200


@student_app.route('/alunos/<int:id_student>')
def get_single_stundent(id_student):
    result = consult_single_student(id_student)

    if result:
        return jsonify(result)

    return jsonify({'erro': 'aluno não encontrado'}), 404


@student_app.route('/alunos/<int:id_student>', methods=["DELETE"])
def del_student(id_student):
    if consult_single_student(str(id_student)):
        delete_student(str(id_student))
        return jsonify({'success': True}), 200

    return jsonify({'erro': 'aluno não encontrado'}), 404


@student_app.route('/alunos/<int:id_student>', methods=["PUT"])
def change_student(id_student):
    if 'nome' not in request.json.keys():
        return jsonify({'erro': 'aluno sem nome'}), 404

    if consult_single_student(str(id_student)):
        update_student(id_student, request.json['nome'])
        return jsonify({'success': True}), 200

    return jsonify({'erro': 'aluno não encontrado'}), 404
