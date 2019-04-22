from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired


class PMSForm(FlaskForm):
    client = StringField("Client", [DataRequired()], render_kw={'class': 'form-control'})
    package = StringField("Package", [DataRequired()], render_kw={'class': 'form-control'})
    fund_pg_select = SelectField("fund_pg_select",
                                 choices=[('fund', 'fund'), ('portgroup', 'pg'), ('file name', 'file')],
                                 render_kw={'class': 'form-control form-control-lg'})
    fund = StringField("fund", [DataRequired()], render_kw={'class': 'form-control'})
    date = DateField("Date", render_kw={'class': 'form-control'})
    directory = StringField("Directory", [DataRequired()], render_kw={'class': 'form-control'})
    tag = StringField("Tag", render_kw={'class': 'form-control'})
    rpt_tag = StringField("Report Tag", render_kw={'class': 'form-control'})
    sector = StringField("Sector/Breakdown", render_kw={'class': 'form-control'})
    cmd_type = SelectField("Command type",
                           choices=[('generic_pms', 'Generic pms rerun'), ('compl', 'Write compliance binary'),
                                    ('exposure')])
    submit = SubmitField("Get the command", render_kw={'class': 'btn btn-default'})
