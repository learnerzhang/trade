from flask import Blueprint, Response
from api_modules.server.models.base import Account, save_entity, get_entities, update_entity
import json

user_blueprint = Blueprint('account', __name__, url_prefix='/account')

def build_filter(args,):
    condictions = []
    code = args.get('code', None)
    if code:
        condictions.append(Account.code == code)

    flag = args.get('flag', None)
    if flag:
        condictions.append(Account.flag == flag)

    date = args.get('date', None)
    if date:
        condictions.append(Account.date == date)

    sell_date = args.get('sell_date', None)
    if sell_date:
        condictions.append(Account.date < sell_date)

    return condictions

def update_act():
    rs = update_entity()
    return rs

def add_act(account):
    return save_entity(account)


def be_acts(args):
    filters = build_filter(args)
    accs = get_entities(Account,filters, Account.date.desc())
    return accs if accs else []


@user_blueprint.route('/get_accounts', methods=['POST', 'GET'])
def get_accounts():

    accs = get_entities(Account, {}, Account.id.asc())
    rs = {'code': 0,'msg': '','data': [ ac.serialize() for ac in accs],}
    return Response(json.dumps(rs), mimetype='application/json')

