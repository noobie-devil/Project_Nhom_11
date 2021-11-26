from flask_wtf import FlaskForm
from wtforms import fields 
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError
import re
class CreateTableForm(FlaskForm):

	def validate_table_name(self, table_name_to_check):
		regex = re.compile("[^a-zA-Z0-9_.-]")
		match = regex.match(table_name_to_check)
		if match:
			raise ValidationError("Invalid input")


	table_name = fields.StringField(label='Table name', validators=[DataRequired(), Length(min=3, max=255)])
	partition_key = fields.StringField(label='Partition Key', validators=[DataRequired(), Length(min=1, max=255)])
	partition_key_type = fields.SelectField("Type: ", choices=[('S','String'), ('N','Number'), ('B','Binary')])
	sort_key = fields.StringField(label='Sort Key - Optional', validators=[DataRequired(), Length(min=1, max=255)])
	sort_key_type = fields.SelectField("Type: ", choices=[('S','String'), ('N','Number'), ('B','Binary')])
	submit = fields.SubmitField(label='Lưu')
	