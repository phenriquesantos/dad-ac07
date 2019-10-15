from flask import Blueprint, request, jsonify

import database

teacher_app = Blueprint('teacher_app', __name__)


def to_dic(rows: list) -> list:
    result = []
    for id, nome in rows:
        result.append({'id': id, 'nome': nome})

    return result


def consult_single_teacher(id: str):
    sql = "SELECT * FROM teacher WHERE id_teacher = ?"
    result = database.consult(sql, (id, ))
    if result:
        return to_dic(result)[0]

    return False


def consult_all_teacher():
    sql = "SELECT * FROM teacher"
    result = database.consult(sql)
    if result:
        return to_dic(result)

    return []


def register_teacher(id, nome):
    sql = "INSERT INTO teacher(id_teacher, nome) VALUES (?, ?)"
    database.register(sql, (id, nome))


def delete_teacher(id):
    sql = "DELETE FROM teacher WHERE id_teacher = ?"
    database.execute(sql, (id, ))
    return True


def update_teacher(id, nome):
    sql = "UPDATE teacher SET nome = ? WHERE id_teacher = ?"
    database.execute(sql, (nome, id))
    return True


@teacher_app.route('/professores')
def get_all_teachers():
    return jsonify(consult_all_teacher())


@teacher_app.route('/professores', methods=["POST"])
def store_teacher():
    new_teacher = request.json
    if 'nome' not in new_teacher.keys():
        return jsonify({'erro': 'professor sem nome'}), 404

    if consult_single_teacher(str(new_teacher['id'])):
        return jsonify({'erro': 'id já utilizada'}), 404

    register_teacher(new_teacher['id'], new_teacher['nome'])
    return jsonify({'success': True}), 200


@teacher_app.route('/professores/<int:id_teacher>')
def get_single_teacher(id_teacher):
    teacher = consult_single_teacher(str(id_teacher))
    if teacher:
        return jsonify(teacher)

    return jsonify({'erro': 'professor não encontrado'}), 404


@teacher_app.route('/professores/<int:id_teacher>', methods=["DELETE"])
def del_teacher(id_teacher):
    if consult_single_teacher(str(id_teacher)):
        delete_teacher(str(id_teacher))
        return jsonify({'success': True})

    return jsonify({'erro': 'professor não encontrado'}), 404


@teacher_app.route('/professores/<int:id_teacher>', methods=["PUT"])
def change_teacher(id_teacher):
    if 'nome' not in request.json.keys():
        return jsonify({'erro': 'professor sem nome'}), 404

    if consult_single_teacher(id_teacher):
        update_teacher(id_teacher, request.json['nome'])
        return jsonify({'success': True})

    return jsonify({'erro': 'professor não encontrado'}), 404
