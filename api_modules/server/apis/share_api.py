from flask import Blueprint, request, current_app, Response
from api_modules.server.models import Share
from api_modules.server.models import get_entities, get_dist_columns, get_nums_by_filter, get_entities_by_filter
from api_modules.server.utils.page_utils import Pagination
import json

share_blueprint = Blueprint('share', __name__, url_prefix='/share')

def build_filter(args):

    condictions = []
    keywords = args.get('keywords', None, type=str)
    if keywords:
        query = str(keywords).replace("\\", "\\\\").replace("%", "\%").replace("'", "\'").replace("_", "\_")
        current_app.logger.debug("query keyword:{}".format(query))
        tokens = query.split(';')
        for token in tokens:
            condictions.append(Share.name.like('%{}%'.format(token)))
    
    industry = args.get('industry', None, type=str)
    if industry:
        condictions.append(Share.industry == industry)

    # username = args.get('username', None, type=str)
    # if username:
    #     condictions.append(Share.username == username)

    # flag = args.get('flag', None, type=int)
    # if flag is not None:
    #     condictions.append(Share.flag == flag)

    return condictions

@share_blueprint.route('/get_all_shares', methods=['POST', 'GET'])
def get_all_shares():
    filters = build_filter(request.args)
    shares = get_entities(cls=Share, filters=filters, order=Share.code.asc())
    rs = {'code': 0,'msg': '','data': [ s.serialize() for s in shares],}
    return Response(json.dumps(rs), mimetype='application/json')


@share_blueprint.route('/industry', methods=['POST', 'GET'])
def get_all_industries():
    results = get_dist_columns(Share, Share.industry)
    rs = {'code': 200,'msg': '','data': [ { 'id':i, 'value': s[0]} for i, s in enumerate(results) if s[0]],}
    return Response(json.dumps(rs), mimetype='application/json')


@share_blueprint.route('/shares', methods=['POST', 'GET'])
def get_shares_by_page():
    page = request.args.get('page', 1, type=int)
    pageSize = request.args.get('limit', 10, type=int)

    filters = build_filter(request.args)
    total = get_nums_by_filter(Share, filters)
    default_order = Share.code.asc()
    

    p = Pagination(current_page=page, total_count=total, page_size=pageSize)
    shares = get_entities_by_filter(Share, filters, p.offset, p.page_size, default_order)

    rs = {'code': 200,'msg': '','data': [ s.serialize() for s in shares],'pagesize': p.page_count, 'totalnum': total}
    return Response(json.dumps(rs), mimetype='application/json')
