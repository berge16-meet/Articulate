from flask import Flask, render_template, request
app = Flask(__name__, static_url_path="", static_folder="static")
from flask import Flask, render_template, request, redirect,url_for
from flask import session as web_session
from flask.ext.wtf import Form, fields, validators
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

from database import Base,User
from sqlalchemy import create_engine
engine=create_engine('sqlite:///Webpage.db')
Base.metadata.create_all(engine)
DBSession=sessionmaker(bind=engine)
session=DBSession()

app.config['SECRET_KEY'] = 'guess who'

db = SQLAlchemy(app)
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
	email = StringField("Email:"[validators.Email()])
	password = PasswordField("Password:" [validators.Required()])
	gender = SelectField("Gender:", choices = [("male", "Male"), ("female", "Female", ("other", "Other"))])
	date_of_birth = DateField("Date of birth:", [validators.Required()])


@app.route('/signup', methods=['GET', 'POST'])
def signup():

	if request.method == 'GET':
		return render_template('signup.html')


	else:
		firstname=request.form['firstname']
		print(firstname)
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
