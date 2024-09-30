from flask import Blueprint, jsonify, request
from app.models.user import User
from app import db 
from app.forms import SettingsForm

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/getusers', methods=['GET'])
def get_users():
    pId = request.args.get('id')
    if pId is not None:
        users = User.query.filter_by(id=pId).all()
        return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])
    else:
        users = User.query.all()
        return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])


@user_bp.route('/deluser', methods=['POST'])
def del_user():
    data = request.get_json()

    if 'username' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    user_del = User.query.filter_by(username=data['username']).first()

    if user_del is None:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user_del)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200

@user_bp.route('/setusers', methods=['POST'])
def post_users():
    data = request.get_json()
    form = SettingsForm(data=data)


    if 'username' not in data or 'email' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    print(form)
    print(data)

    if 'id' in data and data['id']:
        new_user = User.query.filter_by(id=data['id']).first()
        if not new_user:
            return jsonify({'error': 'User not found'}), 404
        new_user.username = form.username.data
        new_user.email = form.email.data
    else:
        new_user = User(
            username=form.username.data,
            email=form.email.data
        )
        db.session.add(new_user)

    db.session.commit()
    return jsonify({'id': new_user.id, 'username': new_user.username, 'email': new_user.email}), 201

