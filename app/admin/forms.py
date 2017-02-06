# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField, ValidationError
from wtforms.validators import DataRequired, Length

class CustomerForm(FlaskForm):
	"""
    Form for admin to add or edit a customer
    """
	name = StringField('Name', validators=[DataRequired()])
	TIN = StringField('TIN',validators=[DataRequired(),Length(min=11, max=11)])
	phone_number = StringField('phone_number',validators=[DataRequired(),Length(min=10, max=10)])
	address = StringField('address', validators=[DataRequired()])
	submit = SubmitField('Submit')

	def validate_TIN(form,field):
		try:
			number = int(field.data)
		except:
			raise ValidationError('Invalid TIN Number')
	def validate_phone_number(form,field):
		try:
			number = int(field.data)
		except:
			raise ValidationError('Invalid Phone Number')

class ItemForm(FlaskForm):
	"""
    Form for admin to add or edit a customer
    """
	name = StringField('Name', validators=[DataRequired()])
	brand = StringField('brand',validators=[DataRequired()])
	price = DecimalField('price',places=2,validators=[DataRequired()])
	
	submit = SubmitField('Submit')

	