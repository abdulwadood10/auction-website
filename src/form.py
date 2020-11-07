from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, BooleanField, SelectField, RadioField,DateField
from wtforms.validators import DataRequired, Length, Email, InputRequired, EqualTo,ValidationError
from flask_wtf.file import FileAllowed, FileField,FileRequired
from src.models import User

class RegisterForm(FlaskForm):
    username = StringField("User Name", validators=[InputRequired('enter user name'), DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators= [InputRequired('enter your email'), DataRequired(), Email()])
    contact = StringField('Contact',validators=[DataRequired(),Length(min=11, max=11)])
    address = TextAreaField('Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken, try something else.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already taken, try something else.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_email(self,email):
        if email.data not in User.get_emails():
            raise ValidationError("This email is not yet registered! Please sign up.")



class ItemForm(FlaskForm):
    item_img = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png','jpeg']),FileRequired()],)
    item_name = StringField('Product Name',validators=[DataRequired()])
    item_desc = TextAreaField('Description', validators=[DataRequired()])
    item_starting_bid = IntegerField('Starting Bid', validators=[DataRequired()])
    item_category = SelectField('Category', validators=[DataRequired()],choices=[('Car','Car'),('Dress','Dress'),('Mobile','Mobile')])
    submit = SubmitField('Create Item')


class BidForm(FlaskForm):
    bidPrice = IntegerField('Bid Price',validators=[DataRequired()])
    # bidStatus = RadioField('Bid Status',choices=[(1,'Active'),(0,'Not Active')],default=1,coerce=int)
    itemID = IntegerField('Item ID',validators=[DataRequired()])
    userName = StringField('Username',validators=[DataRequired()])
    submit = SubmitField('Add Bid')
