from flask import Flask, render_template, request, redirect,url_for
from flask import session as web_session
from wtforms import *
#SubmitField, StringField,PasswordField,TextAreaField, DateField, SelectField,SubmitField, validators
from flask.ext.wtf import Form as WtfForm
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask.ext.bootstrap import Bootstrap
import hashlib
import uuid
from database import Base,User
from sqlalchemy import create_engine

app = Flask(__name__, static_url_path="", static_folder="static")

engine=create_engine('sqlite:///Webpage.db')
Base.metadata.create_all(engine)
DBSessionMaker=sessionmaker(bind=engine)
DBsession=DBSessionMaker()

app.config['SECRET_KEY'] = 'guess who'
app.config['CSRF_ENABLED']=True
WTF_CSRF_ENABLED = True

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)



@app.route('/')
def entry():
	return render_template('entry.html')


class SignUpForm(WtfForm):
	first_name = StringField("First name:")
	last_name = StringField("Last name:")
	email = StringField("Email:", [validators.Email()])
	password = PasswordField("Password:", [validators.Required()])
	gender = SelectField("Gender:", choices = [("male", "Male"), ("female", "Female"), ("other", "Other")])
	date_of_birth = DateField("Date of birth:", [validators.Required()])
	nationality=StringField("Nationality:")
	biography = TextAreaField("Tell us about yourself")
	profile_pic = FileField("You can upload a profile picture.")

	submit = SubmitField("Submit:")

def hash_password(password):
	return hashlib.md5(password.encode()).hexdigest()

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
		password = hash_password(password)
		gender=request.form['gender']
		nationality=request.form['nationality']
		dob=request.form['date_of_birth']
		biography=request.form['biography']

		#profilepic=request.form['profile_pic']
		#user=User(id= 1,firstname='roni',lastname='var',password='jj', email='hello', gender='male',date='1',bio='hi',username='ron',nationality='polish',profilepic='k')
		user=User(firstname=firstname, lastname=lastname,email=email, password=password, gender=gender, nationality=nationality,date=dob,bio=biography)
		DBsession.add(user)
		DBsession.commit()
		print (user.lastname)
		email=DBsession.query(User).filter_by(email=user.email).first().email
		print (email)
		session['id']=uuid.uuid4()
		return redirect(url_for('home',name=firstname))



class Loginform(WtfForm):
	email=StringField('Email:',[validators.Required()])
	password=PasswordField('Password:',[validators.required()])
	submit=SubmitField('Submit')



@app.route('/login',methods=['GET','POST'])
def login():

	loginform=Loginform(csrf_enabled=True)
	def validate(email,password):
		return query.first() != None
	if request.method=='GET':
		return render_template('login.html', form=loginform)
	else:
		email=request.form['email']
		password=request.form['password']

		user_query = DBsession.query(User).filter(User.email.in_([email]), User.password.in_([hash_password(password)]))
		user = user_query.first()
		if user != None:
			session['id']=uuid.uuid4()
			return redirect(url_for('home',name=user.firstname))
		return render_template('login.html',form=loginform)




'''
	loger=DBsession.query(User).filter_by(email=email)
	if DBsession.query(User).filter_by(email=loger.email)!=None:
		if loger.password==DBsession.query(User).filter_by(email=loger.email).password:
			return redirect (url_for('home',name=DBsession.query(User).filter_by(email=loger.email).firstname))
'''

@app.route('/user/<name>')
def profile(name):
	user = DBsession.query(User).filter_by(firstname = name).first()
	myPhotos = DBsession.query(Gallery).filter_by(user_id = user.id).all()
	return render_template('profile.html', name = name, posts = myPhotos)


class CommentForm(WtfForm):
	comment=TextAreaField('Comment:', [validators.Length(min = 20, max = 4000), validators.Required()])

@app.route('/home/<name>')
def home(name):
	return render_template('home.html', name = name)


@app.route ('/canvas/user/<name>')
def canvas(name):
	return render_template('canvas.html', name = name)

@app.route ('/chat/user/<name>')
def chat(name):
	return render_template('chat.html')
@app.route ('/about')
def about():
	return render_template('about.html')

@app.route ('/contact')
def contact():
	return render_template('contact.html')

@app.route('/profile')
def uploads():
    posts = [
        {
            'picture': "static/images.jpeg",
            'user': "Hila Tal",
            'titile': "me n staff",
            'num_of_likes': "15"
        },
        {
            'picture': "static/hillarycari.jpg",
            'user': "Marvin",
            'title': "something meaningful",
            'num_of_likes': "20"
        },
        {
            'picture': "static/bibi.jpg",
            'user': "Neta Ravid",
            'title': "titletitletitle",
            'num_of_likes': "4"
        },
        {
            'picture': "static/bibi.jpg",
            'user': "Berge hagopian",
            'title': "berge has a weird last name",
            'num_of_likes': "10"
        },
        {
            'picture': "static/bibi.jpg",
            'user': "Hila Tal",
            'title': "the 5th post",
            'num_of_likes': "11"
        },
        {
            'picture': "static/papir_iroszer.jpg",
            'user': "Hila Tal",
            'title': "the previouse background image",
            'num_of_likes': "17"
        }
    ]

    return render_template('profile.html', posts=posts)

class CommentForm(WtfForm):
	comment=TextAreaField('Comment:', [validators.Length(min = 20, max = 4000), validators.Required()])

if __name__ == '__main__':
	app.run(debug=True)
