# from flask_wtf import FlaskForm 
# importing from flask_wtforms library the flaskform att 
from wtforms import Form, StringField, PasswordField , SubmitField, BooleanField
# in forms when the input id=s going to be a string use stringfield option 
from wtforms.validators import DataRequired,Length,Email,EqualTo
#validators are used to validate a response in a form ie datareq for taking data is complusory and lenght for wordlimit etc

class CommRegistration(Form): # making a class for reg forms 

    username = StringField('Committee-Name' , validators=[DataRequired(),Length(min ='2',max='50')])
    id = StringField('Committee-ID' , validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password ', validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')

class CommLogin(Form): # making a class for reg forms 
 
    username = StringField('Committee-Name' , validators=[DataRequired(),Length(min ='2',max='50')])
    id = StringField('Committee-ID' , validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    remember= BooleanField('Remember me ')
    submit=SubmitField('Login')

class AdminRegistration(Form): # making a class for reg forms 

    username = StringField('Admin-Name' , validators=[DataRequired(),Length(min ='2',max='50')])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password=PasswordField('Password', validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password ', validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')

class AdminLogin(Form): # making a class for reg forms 

    username = StringField('Admin-Name' , validators=[DataRequired(),Length(min ='2',max='50')])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password=PasswordField('Password', validators=[DataRequired()])
    remember= BooleanField('Remember me ')
    submit=SubmitField('Login')
