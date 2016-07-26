from flask import Flask, render_template, request
app = Flask(__name__, static_url_path="", static_folder="static")
from flask import Flask, render_template, request, redirect,url_for
from flask import session as web_session
from wtforms import *
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)

from database import Base,User
from sqlalchemy import create_engine
engine=create_engine('sqlite:///Webpage.db')
Base.metadata.create_all(engine)
DBSession=sessionmaker(bind=engine)
session=DBSession()

app.config['SECRET_KEY'] = 'guess who'

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
'''
if session.query.all()=null:#no users exist:
	users = [
		{
			firstname: 'asdfasd',

		}
	]

	# for user in users
	insertUser = User(fisrname = user.firstname, las)
	#user1=User(

	session.commit()
'''
@app.route('/')
def entry():
	return render_template('entry.html')


class SignUpForm(Form):
	first_name = StringField("First name:")
	last_name = StringField("Last name:")
	email = StringField("Email:", [validators.Email()])
	password = PasswordField("Password:", [validators.Required()])
	gender = SelectField("Gender:", choices = [("male", "Male"), ("female", "Female"), ("other", "Other")])
	date_of_birth = DateField("Date of birth:", [validators.Required()])
	biography = TextAreaField("Tell us about yourself")
	profile_pic = FileField("You can upload a profile picture.")

	submit = SubmitField("Submit:")


@app.route('/signup', methods=['GET', 'POST'])
def signup():

	signup_form = SignUpForm()
	if request.method == 'GET':
		return render_template('signup.html', form = signup_form)


	else:
		firstname=request.form['first_name']

		lastname=request.form['last_name']
		email=request.form['email']
		password=request.form['password']
		gender=request.form['gender']

		dob=request.form['date_of_birth']
		biography=request.form['biography']

		#profilepic=request.form['profile_pic']
		print(firstname)
		#user=User(id= 1,firstname='roni',lastname='var',password='jj', email='hello', gender='male',date='1',bio='hi',username='ron',nationality='polish',profilepic='k')
		user=User(firstname=firstname, lastname=lastname,email=email, password=password, gender=gender, date=dob,bio=biography)
		session.add(user)
		session.commit()
		print (user.lastname)
		email=session.query(User).filter_by(email=user.email).first().email
		print (email)
		return redirect(url_for('home',name=firstname))
		


class Loginform(Form):
	email=StringField('email:')
	password=StringField('password:')
	submit=SubmitField('Submit')
@app.route('/login',methods=['GET','POST'])


@app.route('/login')
def login():
	loginform=Loginform()
	def validate(email,password):
		query= Session.query(User).filter(User.email.in_([email]),
		User.password.in_([password])	)
		return query.first() != None

	if request.method=='GET':
		return render_template('login.html', form=loginform)
	email=str(request.form['email'])
	password=str(request.form['password'])
	is_valid=validate(email.password)
	#if is_valid==False:
		
@app.route('/user/<name>')
def profile(name):
	return render_template('profile.html', name = name)

@app.route('/home/user/<name>')
def home(name):
	return render_template('home.html', name=name)

@app.route ('/canvas/user/<name>')
def canvas(name):
	return render_template('canvas.html', name=name)

@app.route ('/chat/user/<name>')
def chat(name):
	return render_template('chat.html')






if __name__ == '__main__':
	app.run(debug=True)
