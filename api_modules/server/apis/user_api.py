from flask import Blueprint, Response
from api_modules.server.models.base import User, save_entity, get_entities, get_entity, update_entity
import json

user_blueprint = Blueprint('user', __name__, url_prefix='/user')


def build_filter(args,):
    condictions = []
    name = args.get('name', 'niu_x', )
    if name:
        condictions.append(User.name == name)
    return condictions


def get_user(name=None):
    filters = build_filter({'name': name})
    results = get_entity(User, filters)
    if results:
        return results[0]
    else:
        return None

def update_user():
    rs = update_entity()
    return rs

@user_blueprint.route('/add_user', methods=['POST', 'GET'])
def add_user():
    user = User("niu_x", email='new_x@trade.com', cash=500000)
    rs = {'code': 200,'msg':'', 'data': [],}
    if save_entity(user):
        rs.update({"msg": 'sucess'})
    else:
        rs.update({"msg": 'user exists'})
    return Response(json.dumps(rs), mimetype='application/json')



@user_blueprint.route('/get_users', methods=['POST', 'GET'])
def get_all_users():
    uers = get_entities(User, [], User.id.asc())
    rs = {'code': 0,'msg': '','data': [ u.serialize() for u in uers],}
    return Response(json.dumps(rs), mimetype='application/json')


if __name__ == "__main__":
    u = get_user(name='niu_x')
    print(u)
    u.set_name('niu')
    update_user()
    u = get_user(name='niu')
    print(u)
