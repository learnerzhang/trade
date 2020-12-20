import click
import logging
from flask.cli import with_appcontext
from api_modules.server.models import init_db
from api_modules.server.pipeline.stg_run import train, predict
from api_modules.server import get_all_stock_names, get_all_stock_industries, update_trades
from stock_analytic_modules.static_trade import run_pipline_stg
from api_modules.server.pipeline.persist_flow import syncup_transaction
from api_modules.server.pipeline.trade_run import trade_run
from api_modules.server import init_trade_date, gen_dataset
from api_modules.server.utils.config import ConfigUtils

logging.basicConfig(format='%(asctime)s %(message)s', filename='sequoia.log')
logging.getLogger().setLevel(logging.INFO)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


@click.command('init-stock')
@with_appcontext
def init_stocks():
    # date
    init_trade_date()
    # stock names
    get_all_stock_names()
    # industries
    get_all_stock_industries()
    # syncup
    update_trades()
    click.echo('Initialized the stocks.')


@click.command('syncup-stock')
@with_appcontext
def syncup_stocks():
    syncup_transaction()
    click.echo('Syncup the stocks.')


@click.command('run-stg')
@with_appcontext
def run_stg():
    run_pipline_stg()
    click.echo('Update the strategy.')


@click.command('run-gen-ds')
@with_appcontext
def run_gen_ds():
    gen_dataset()
    click.echo("finish dataset {}!".format(ConfigUtils.get_stock("STOCKS_DATESET")))


@click.command('train')
@with_appcontext
def run_train():
    train()
    click.echo('finish train model.')


@click.command('predict')
@with_appcontext
def run_predict():
    predict()
    click.echo('finish predict model.')



@click.command('trade-run')
@with_appcontext
def run_trade():
    trade_run()
    click.echo('finish trade.')


@click.command('help')
@with_appcontext
def help():
    click.echo('flask [init-db|run-std|test|run|help]')


def bind_app(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(run_stg)
    app.cli.add_command(init_stocks)
    app.cli.add_command(syncup_stocks)
    app.cli.add_command(run_train)
    app.cli.add_command(run_predict)
    app.cli.add_command(run_gen_ds)
    app.cli.add_command(run_trade)
    
    app.cli.add_command(help)
