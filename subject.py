from flask import request, Blueprint, jsonify
from validacao import validar_campos
from teacher import get_single_teacher
subject_db = []
subject_app = Blueprint('subject_app', __name__)

@subject_app.route('/disciplinas')
def get_all_subject():
    return jsonify(subject_db), 200

@subject_app.route('/disciplinas', methods=['POST'])
def store_subject():
    new_subject = request.json
    validate_data = { 'id': int, 'nome': str, 'status': int, 'plano_ensino': str, 'carga_horaria': int }

    if 'id_coordenador' in new_subject.keys():
        validate_data['id_coordenador'] = int
        result, status_code = get_single_teacher(new_subject['id_coordenador'])
        if status_code == 404:
            return jsonify({ 'erro': True }), 404

    if not validar_campos(new_subject, validate_data):
        return jsonify({ 'erro': True }), 404

    for subject in subject_db:
        if subject['id'] == new_subject['id']:
            return jsonify({ 'erro': 'id já utilizada' }), 404

    subject_db.append(new_subject)
    return jsonify({ 'success': True }), 200

@subject_app.route('/disciplinas/<int:subject_id>')
def get_single_subect(subject_id):
    for subject in subject_db:
        if subject_id == subject['id']:
            return jsonify(subject), 200

    return jsonify({ 'erro': 'disciplina não encontrada' }), 404

@subject_app.route('/disciplinas/<int:subject_id>', methods=['DELETE'])
def del_subject(subject_id):
    for subject in subject_db:
        if subject_id == subject['id']:
            subject_db.remove(subject)
            return jsonify({'success': True}), 200

    return jsonify({ 'erro': 'disciplina não encontrada' }), 404


@subject_app.route('/disciplinas/<int:subject_id>', methods=["PUT"])
def change_subject(subject_id):
    if not 'nome' in request.json.keys():
        return jsonify({ 'erro': True }), 404

    new_subject = request.json

    for subject in subject_db:
        if subject['id'] == subject_id:
            subject['nome'] = new_subject['nome']
            
            return jsonify({ 'success': True })

    return jsonify({ 'erro': 'disciplina não encontrada' }), 404

    
