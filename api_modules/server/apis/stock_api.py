from flask import Blueprint, jsonify, request, current_app, session, Response, render_template
import json

stock_blueprint = Blueprint('stock', __name__)


@stock_blueprint.route('/get_all_stocks', methods=['POST', 'GET'])
def get_all_stocks():
    rs = {'code': 0,'msg': '','data': [],}
    return Response(json.dumps(rs), mimetype='application/json')