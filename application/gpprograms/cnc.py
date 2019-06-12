from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired
from datetime import date
import datetime


class CNC:
    def __init__(self, form: FlaskForm = None):
        self.form = form
        yyyymmdd_date = datetime.datetime.strftime(form.date.data, '%Y%m%d')
        client = form.client.data.upper()
        tag = form.tag.data.upper()
        package = form.package.data.upper()
        sector = form.sector.data.upper()
        if form.fund_pg_select.data != 'file':
            fund = form.fund.data.upper()
        self.commands = {
            'generic_cnc': """ cnc_batch.pl -{fund_pg_select} {fund} -cmd "{date} -fund_level 10 -mid_level_funds -show_ticker -fund_html_rpt gp -fund_htlink_dir . -W {report_tag}.{breakdown}" -tag "{tag}" -dir {directory} -pkg {package} """.format(
                fund_pg_select=form.fund_pg_select.data,
                fund=fund,
                date=yyyymmdd_date,
                report_tag=form.rpt_tag.data,
                breakdown=form.sector.data,
                package=package,
                directory=form.directory.data,
                tag=tag),
            'cnc_ifile_parser': """ifile_parse.pl -rpt {report_tag} -bd {breakdown} -depth {depth} -cnc -db -client {client} -client_tree {client_tree} -pkg {package} > /d0/prod1/reports/test/{report_tag}_{breakdown}.ifile""".format(
                report_tag=form.rpt_tag.data,
                breakdown=form.sector.data,
                depth=form.depth.data,
                client=client,
                client_tree=client,
                package=package
            ),
            'cnc_custom_var': """
            :mid_level_funds Y
            :no_pg_html Y
            :enable_gppos_link Y
            :use_brk_title Y            
            :fund_htlink_dir .
            :show_all_sectors N
            :show_ticker Y
            :fund_level 10
            :suppress_cash_no_short Y
            :load_port_risk Y
            :var_use_gp N
            :exp_hi {exp_hi}
            :var_type {var_type}
            :{var_history} {var_history_count}
            :var_decay_daily {var_decay_daily}
            :var_calendar {var_calendar}
            W smi_var_99_10day_sum
            :var_mat_date {var_mat_date}
            :econ_date {econ_date}
            W smi_svar_99_10day            
            """.format(exp_hi=form.exp_hi.data,
                       var_type=form.var_type.data,
                       var_history=form.var_history.data,
                       var_history_count=form.var_history_count.data,
                       var_decay_daily=form.var_decay_daily.data,
                       var_calendar=form.var_calendar.data,
                       var_mat_date=form.var_mat_date.data,
                       econ_date=form.econ_date.data)

        }

    def convert_to_html(self, command_arr):
        command_arr[0] = '<span class="command_keyword">' + command_arr[0] + '</span>'
        for i in range(len(command_arr)):
            if command_arr[i][0] == '-':
                command_arr[i] = '<span class="command_switch">' + command_arr[i] + '</span>'
        command_html = " ".join(command_arr)
        return command_html

    def get_html_command(self):
        command = self.commands[self.form.cmd_type.data]
        command_arr = command.split()
        return self.convert_to_html(command_arr)

    def get_command(self):
        return self.commands[self.form.cmd_type.data]


class CNCForm(FlaskForm):
    commands = [('generic_cnc', 'Generic cnc_batcher command'),
                ('cnc_ifile_parser', 'cnc ifile parser'),
                ('cnc_custom_var', 'cnc custom var')
                ]
    client = StringField("Client", [DataRequired()],
                         render_kw={'class': 'form-control', 'style': 'text-transform:uppercase'})
    package = StringField("Package", [DataRequired()],
                          render_kw={'class': 'form-control', 'style': 'text-transform:uppercase'})
    fund_pg_select = SelectField("fund_pg_select",
                                 choices=[('fund', 'fund'), ('pg', 'portgroup'), ('file', 'file of funds')],
                                 render_kw={'class': 'form-control form-control-lg'})
    fund = StringField("fund", [DataRequired()], render_kw={'class': 'form-control'})
    date = DateField("Date", default=date.today(), format='%Y%m%d', render_kw={'class': 'form-control'})
    directory = StringField("Directory", render_kw={'class': 'form-control',
                                                    'placeholder': 'If kept blank auto populated'})
    tag = StringField("Tag", render_kw={'class': 'form-control', 'placeholder': 'If kept blank auto populated'})
    rpt_tag = StringField("Report Tag", render_kw={'class': 'form-control'})
    sector = StringField("Sector/Breakdown", render_kw={'class': 'form-control', 'style': 'text-transform:uppercase'})
    depth = StringField("Breakdown depth", render_kw={'class': 'form-control'})
    # var related columns
    exp_hi = StringField("Exposure hierarchy", render_kw={'class': 'form-control'})
    var_type = SelectField("VaR type",
                           choices=[('DLY', 'Daily'), ('WKL', 'Weekly'), ('WKC', 'Weekly Custom')],
                           render_kw={'class': 'form-control form-control-lg'})
    var_history = SelectField("VaR type",
                              choices=[('var_history_daily', 'VaR History Daily'), ('var_history_weekly', 'VaR History Weekly')],
                              render_kw={'class': 'form-control form-control-lg'})
    var_history_count = StringField("VaR History Count", render_kw={'class': 'form-control'})
    var_decay_daily = StringField("VaR Decay Daily", render_kw={'class': 'form-control'})
    var_calendar = StringField("VaR Calendar", render_kw={'class': 'form-control'})
    var_mat_date = StringField("VaR Matrix date", render_kw={'class': 'form-control'})
    econ_date = StringField("Econ date", render_kw={'class': 'form-control'})
    cmd_type = SelectField("Command type", choices=commands, render_kw={'class': 'form-control form-control-lg'})
    submit = SubmitField("Get the command", render_kw={'class': 'btn btn-default'})
