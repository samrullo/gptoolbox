from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired


class PMS:
    def __init__(self, form: FlaskForm = None):
        self.form = form
        self.commands = {
            'generic_pms': """pms_batch.pl -{fund_pg_select} {fund} -cmd "{date} -gpsettings GP:DAILY -ignorePublish" -pkg {pkg} -dir {directory} -tag "{tag}" """.format(
                fund_pg_select=form.fund_pg_select.data,
                fund=form.fund.data,
                date=form.date.data,
                pkg=form.package.data,
                directory=form.directory.data,
                tag=form.tag.data),
            'compl_pms': """ startPCS.pl {fund} {date} -loadProdGroups -gpsettings GP:BINARY -pkg {package} -complBin -ignorePublish """.format(
                fund=form.fund.data,
                date=form.date.data,
                package=form.package.data),
            'exposure_pms': """pms_batch.pl -{fund_pg_select} {fund} -cmd "{date} -gpsettings GP:DAILY:i -save_exposure -save_exp_purpose P100 -ignorePublish" -pkg {pkg} -dir {directory} -tag "{tag}" """.format(
                fund_pg_select=form.fund_pg_select.data,
                fund=form.fund.data,
                date=form.date.data,
                pkg=form.package.data,
                directory=form.directory.data,
                tag=form.tag.data),
            'sector_pms': """pms_batch.pl -{fund_pg_select} {fund} -cmd "{date} -gpsettings GP:DAILY:i -writeSectorMap {sector} -ignorePublish" -pkg {pkg} -dir {directory} -tag "{tag}" """,
            'port_totals': """pms_batch.pl -{fund_pg_select} {fund} -cmd "{date} -gpsettings GP:DAILY:i -saveTotals {rpt_tag} -ignorePublish" -pkg {pkg} -dir {directory} -tag "{tag}" """,
            'composite_bench_pms': """pms_batch.pl -{fund_pg_select} {fund} -cmd "{date} -gpsettings GP:DAILY:i -benchmark -loadProdGroups -W {rpt_tag}.{sector} -ignorePublish" -pkg {pkg} -dir {directory} -tag "{tag}" """
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


class PMSForm(FlaskForm):
    commands = [('generic_pms', 'Generic pms that updates ppd,gpx, and recreated pms binary'),
                ('compl_pms', 'To recreate compliance binary only'),
                ('exposure_pms', 'Save portfolio exposure'),
                ('sector_pms', 'Update sector/breakdown'),
                ('port_totals', 'Save to port totals'),
                ('composite_bench_pms', 'Write pms on composite benchmark')]
    client = StringField("Client", [DataRequired()], render_kw={'class': 'form-control', 'value': 'myclient'})
    package = StringField("Package", [DataRequired()], render_kw={'class': 'form-control'})
    fund_pg_select = SelectField("fund_pg_select",
                                 choices=[('fund', 'fund'), ('portgroup', 'pg'), ('file name', 'file')],
                                 render_kw={'class': 'form-control form-control-lg'})
    fund = StringField("fund", [DataRequired()], render_kw={'class': 'form-control'})
    date = StringField("Date", render_kw={'class': 'form-control'})
    directory = StringField("Directory", render_kw={'class': 'form-control',
                                                    'placeholder': 'If kept blank, this will be auto generated'})
    tag = StringField("Tag", render_kw={'class': 'form-control'})
    rpt_tag = StringField("Report Tag", render_kw={'class': 'form-control'})
    sector = StringField("Sector/Breakdown", render_kw={'class': 'form-control'})
    cmd_type = SelectField("Command type", choices=commands, render_kw={'class': 'form-control form-control-lg'})
    submit = SubmitField("Get the command", render_kw={'class': 'btn btn-default'})
