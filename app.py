#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-07-29 09:17
# @Author  : zhangzhen
# @Site    :
# @File    : server.py
# @Software: PyCharm

from flask import Flask, logging
import os
from api_modules.server.apis import fund_api, stock_api, transaction_api, user_api
from api_modules.server.apis import share_api
from cmd import bind_app

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
logger = logging.create_logger(app)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # init db
    bind_app(app)

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    app.register_blueprint(user_api.user_blueprint)
    app.register_blueprint(transaction_api.transaction_blueprint)
    app.register_blueprint(stock_api.stock_blueprint)
    app.register_blueprint(share_api.share_blueprint)
    app.register_blueprint(fund_api.fund_blueprint)
    return app


app = create_app()
app.debug = True
app.run(port=8000)

if __name__ == '__main__':
    # init_db()
    # http_server = WSGIServer(('', port), app)
    # http_server.serve_forever()
    pass
