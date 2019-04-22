from application import app
from flask import render_template, redirect
from application.gpprograms.pms import PMSForm, PMS
import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)
logging.basicConfig()


@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/pms", methods=['GET', 'POST'])
def pms():
    _logger.info("Starting pms route...")
    form = PMSForm()
    command = ""
    html_command = ""
    if form.validate_on_submit():
        _logger.info("Tag data is :{}".format(form.tag.data))
        pms = PMS(form=form)
        command = pms.get_command()
        html_command = pms.get_html_command()
    else:
        _logger.info("validation was unsuccessful...")
    return render_template("pms_template.html", form=form, command=command, html_command=html_command)


@app.route("/cnc")
def cnc():
    return render_template("pms_template.html")


@app.route("/risk")
def risk():
    return render_template("pms_template.html")
