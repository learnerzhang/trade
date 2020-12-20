from flask import Blueprint, jsonify, request, current_app, session, Response, render_template
import json

fund_blueprint = Blueprint('fund', __name__)


@fund_blueprint.route('/get_all_funds', methods=['POST', 'GET'])
def get_all_funds():
    rs = {'code': 0,'msg': '','data': [],}
    return Response(json.dumps(rs), mimetype='application/json')