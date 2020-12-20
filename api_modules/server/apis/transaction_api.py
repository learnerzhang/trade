from flask import Blueprint, request, current_app, Response
from api_modules.server.models import Transaction, Share
from api_modules.server.models import get_nums_by_filter, get_entities_by_filter, get_recently_trade_date, get_tbs_nums_by_filter, get_tbs_entities_by_filter, get_entity_by_filter
from api_modules.server.utils.page_utils import Pagination
import json

transaction_blueprint = Blueprint('transaction', __name__, url_prefix='/tran')

def build_filter(args, trade_date=None):

    condictions = []
    keywords = args.get('keywords', None, type=str)
    if keywords:
        query = str(keywords).replace("\\", "\\\\").replace("%", "\%").replace("'", "\'").replace("_", "\_")
        current_app.logger.debug("query keyword:{}".format(query))
        tokens = query.split(';')
        for token in tokens:
            condictions.append(Transaction.name.like('%{}%'.format(token)))
    
    code = request.args.get('code', None, type=str)
    if code:
        condictions.append(Transaction.code == code)

    industry = request.args.get('industry', None, type=str)
    if industry:
        condictions.append(Share.industry == industry)

    if trade_date:
        condictions.append(Transaction.date == trade_date)

    
    # username = args.get('username', None, type=str)
    # if username:
    #     condictions.append(Share.username == username)

    # flag = args.get('flag', None, type=int)
    # if flag is not None:
    #     condictions.append(Share.flag == flag)

    return condictions

def build_order(args):
    default_order = Transaction.code.asc

    field = args.get('field', None, type=str)
    order = args.get('order', None, type=int)
    if field == 'close':
        default_order = Transaction.close.asc if order == 1 else Transaction.close.desc
    elif field == 'pctChg':
        default_order = Transaction.pctChg.asc if order == 1 else Transaction.pctChg.desc
    elif field == 'high':
        default_order = Transaction.high.asc if order == 1 else Transaction.high.desc
    elif field == 'low':
        default_order = Transaction.low.asc if order == 1 else Transaction.low.desc
    elif field == 'volume':
        default_order = Transaction.volume.asc if order == 1 else Transaction.volume.desc
    elif field == 'amount':
        default_order = Transaction.amount.asc if order == 1 else Transaction.amount.desc
    return default_order

@transaction_blueprint.route('/get_all_transactions', methods=['POST', 'GET'])
def get_all_transactions():
    dt = get_recently_trade_date()
    rs = {'code': 200,'msg': '','data': [],}
    return Response(json.dumps(rs), mimetype='application/json')

@transaction_blueprint.route('/get_tran', methods=['POST', 'GET'])
def get_share_tran():
    dt = get_recently_trade_date()
    filters = build_filter(request.args, trade_date=dt[0].calendar_date)
    enities = get_entity_by_filter(Transaction, filters=filters)
    rs = {'code': 200,'msg': '',}
    if enities:
        rs.update({"data": enities[0].serialize()})
    else:
        rs.update({"data": []})
    return Response(json.dumps(rs), mimetype='application/json')

@transaction_blueprint.route('/daily_trans', methods=['POST', 'GET'])
def get_daily_trans_by_page():

    dt = get_recently_trade_date()
    page = request.args.get('page', 1, type=int)
    pageSize = request.args.get('limit', 10, type=int)
    filters = build_filter(request.args, trade_date=dt[0].calendar_date)

    industry = request.args.get('industry', None, type=str)
    if industry:
        total = get_tbs_nums_by_filter(Transaction, Share, Transaction.code, Share.code, filters)
        p = Pagination(current_page=page, total_count=total, page_size=pageSize)
        default_order = build_order(request.args)
        trans = get_tbs_entities_by_filter(Transaction, Share, Transaction.code, Share.code, filters, p.offset, p.page_size, default_order())
    else:
        total = get_nums_by_filter(Transaction, filters)
        p = Pagination(current_page=page, total_count=total, page_size=pageSize)
        default_order = build_order(request.args)
        trans = get_entities_by_filter(Transaction, filters, p.offset, p.page_size, default_order())

    rs = {'code': 200,'msg': '','data': [ s.serialize() for s in trans],'pagesize': pageSize, 'page': page, 'totalpages':p.page_count, 'totalnum':total}
    return Response(json.dumps(rs), mimetype='application/json')


@transaction_blueprint.route('/trans', methods=['POST', 'GET'])
def get_trans_by_page():
    page = request.args.get('page', 1, type=int)
    pageSize = request.args.get('limit', 10, type=int)
    filters = build_filter(request.args)
    total = get_nums_by_filter(Transaction, filters)

    p = Pagination(current_page=page, total_count=total, page_size=pageSize)
    trans = get_entities_by_filter(Transaction, filters, p.offset, p.page_size, Transaction.code.asc())

    rs = {
        'code': 200,
        'msg': '',
        'pagesize': pageSize,
        'totalpages':p.page_count,
        'page': page,
        'data': [ s.serialize() for s in trans],
    }
    return Response(json.dumps(rs), mimetype='application/json', headers={"Set-Cookie": "HttpOnly;Secure;SameSite=Strict"})
