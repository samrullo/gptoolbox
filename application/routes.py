from application import app
from flask import render_template, redirect, session, url_for
from application.gpprograms.pms import PMSForm, PMS
import logging
import datetime
from sqlalchemy import create_engine
import pandas as pd

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)
logging.basicConfig()


@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    return render_template("index.html", home=True)


@app.route("/query")
def query():
    engine = create_engine('sqlite:///application/db/gptoolbox.db')
    df = pd.read_sql("select * from queries", engine)
    _logger.info("First rows of dataframe:{}".format(df.head()))
    return render_template('queries.html', queries=df, query=True)


@app.route("/pms", methods=['GET', 'POST'])
def pms():
    _logger.info("Starting pms route...")
    form = PMSForm()
    if form.client.data != session.get('client') and form.client.data:
        session['client'] = form.client.data
    if form.package.data != session.get('package') and form.package.data:
        session['package'] = form.package.data
    if form.client.data != 'BEN':
        if not form.directory.data:
            form.directory.data = '/d0/reports/gp_reports/MAIN/{}'.format(
                datetime.datetime.strftime(form.date.data, '%Y%m%d'))
    if not form.tag.data:
        form.tag.data = '{} : {} running scratch'.format(form.client.data, form.fund.data)
    form.client.data = session.get('client')
    form.package.data = session.get('package')
    command = ""
    html_command = ""
    if form.validate_on_submit():
        # session['pms'] = {'client': form.client.data.upper, 'package': form.package.data}
        session.pop('client', None)
        session['client'] = form.client.data
        _logger.info("Tag data is :{}".format(form.tag.data))
        pms = PMS(form=form)
        command = pms.get_command()
        html_command = pms.get_html_command()
    else:
        _logger.info("validation was unsuccessful...")
    return render_template("pms_template.html", form=form, command=command, html_command=html_command, pms=True)


@app.route("/cnc")
def cnc():
    return render_template("pms_template.html")


@app.route("/risk")
def risk():
    return render_template("pms_template.html")
