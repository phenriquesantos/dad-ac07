from flask import request, Blueprint, jsonify
from validacao import validar_campos
from teacher import consult_single_teacher

import database

subject_app = Blueprint('subject_app', __name__)


def to_dic(rows: list) -> list:
    result = []
    for id, nome, status, plano_ensino, carga_horaria, id_coordenador in rows:
        result.append({
            'id': id,
            'nome': nome,
            'status': status,
            'plano_ensino': plano_ensino,
            'carga_horaria': carga_horaria,
            'id_coordenador': id_coordenador
        })

    return result


def consult_single_subject(id: str):
    sql = "SELECT * FROM subject WHERE id_subject = ?"
    result = database.consult(sql, (id, ))
    if result:
        return to_dic(result)[0]

    return False


def consult_all_subject():
    sql = "SELECT * FROM SUBJECT"
    result = database.consult(sql)
    if result:
        return to_dic(result)

    return []


def register_subject(id, nome, status, plano_ensino,
                     carga_horaria, id_coordenador=None):
    sql = """
        INSERT INTO subject(id_subject,
        nome,
        status,
        plano_ensino,
        carga_horaria,
        id_coordenador) VALUES (?, ?, ?, ?, ?, ?)
    """
    database.register(sql, (id, nome, status, plano_ensino,
                      carga_horaria, id_coordenador))


def delete_subject(id):
    sql = "DELETE FROM subject WHERE id_subject = ?"
    database.execute(sql, (id, ))
    return True


def update_subject(id, nome):
    sql = "UPDATE subject SET nome = ? WHERE id_subject = ?"
    database.execute(sql, (nome, id))
    return True


@subject_app.route('/disciplinas')
def get_all_subject():
    return jsonify(consult_all_subject()), 200


@subject_app.route('/disciplinas', methods=['POST'])
def store_subject():
    new_subject = request.json
    id_coordenador = None
    validate_data = {'id': int, 'nome': str, 'status': int,
                     'plano_ensino': str, 'carga_horaria': int}

    if 'id_coordenador' in new_subject.keys():
        validate_data['id_coordenador'] = int
        id_coordenador = new_subject['id_coordenador']
        result = consult_single_teacher(
                                new_subject['id_coordenador'])
        if not result:
            return jsonify({'erro': True}), 404

    if not validar_campos(new_subject, validate_data):
        return jsonify({'erro': True}), 404

    if consult_single_subject(new_subject['id']):
        return jsonify({'erro': 'id já utilizada'}), 404

    register_subject(
            new_subject['id'], new_subject['nome'],
            new_subject['status'], new_subject['plano_ensino'],
            new_subject['carga_horaria'], id_coordenador
        )
    return jsonify({'success': True}), 200


@subject_app.route('/disciplinas/<int:subject_id>')
def get_single_subect(subject_id):
    subject = consult_single_subject(subject_id)
    if subject:
        return jsonify(subject), 200

    return jsonify({'erro': 'disciplina não encontrada'}), 404


@subject_app.route('/disciplinas/<int:subject_id>', methods=['DELETE'])
def del_subject(subject_id):
    subject = consult_single_subject(subject_id)
    if subject:
        delete_subject(subject_id)
        return jsonify({'success': True}), 200

    return jsonify({'erro': 'disciplina não encontrada'}), 404


@subject_app.route('/disciplinas/<int:subject_id>', methods=["PUT"])
def change_subject(subject_id):
    if 'nome' not in request.json.keys():
        return jsonify({'erro': True}), 404

    new_subject = request.json
    subject = consult_single_subject(subject_id)
    if subject:
        update_subject(subject_id, new_subject['nome'])
        return jsonify({'success': True})

    return jsonify({'erro': 'disciplina não encontrada'}), 404
