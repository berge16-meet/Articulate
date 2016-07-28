from flask import Flask, render_template, request, session
app = Flask(__name__, static_url_path="", static_folder="static")
from flask import Flask, render_template, request, redirect,url_for
from flask import session as web_session
from wtforms import *
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask.ext.bootstrap import Bootstrap
import hashlib
import uuid


from database import Base,User,Gallery,Comment
from sqlalchemy import create_engine


app = Flask(__name__)

from database import Base,User
from sqlalchemy import create_engine
engine=create_engine('sqlite:///Webpage.db')
Base.metadata.create_all(engine)
DBSessionMaker=sessionmaker(bind=engine)
DBsession=DBSessionMaker()

app.config['SECRET_KEY'] = 'guess who'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)



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
		email=DBsession.query(User).filter_by(email=user.email).first().email
		session['id']=uuid.uuid4()
		return redirect(url_for('home',name=firstname))



class Loginform(Form):
	email=StringField('Email:',[validators.Required()])
	password=PasswordField('Password:',[validators.required()])
	submit=SubmitField('Submit')



@app.route('/login',methods=['GET','POST'])
def login():

	loginform=Loginform(csrf_enabled=True)

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
			return redirect(url_for('home',name=user.username))

		return render_template('login.html',form=loginform)




'''
	loger=DBsession.query(User).filter_by(email=email)
	if DBsession.query(User).filter_by(email=loger.email)!=None:
		if loger.password==DBsession.query(User).filter_by(email=loger.email).password:
			return redirect (url_for('home',name=DBsession.query(User).filter_by(email=loger.email).firstname))
'''

@app.route('/user/<name>')
def profile(name):
	return render_template('profile.html', name = name)

class CommentForm(Form):
	comment=TextAreaField('Comment:', [validators.Length(min = 20, max = 4000), validators.Required()])


# @app.route('/post/<int:post_id>', methods=['GET','POST'])
# def post(post_id):

# 	if request.method == 'GET':
# 		post = DBsession.query(Gallery).filter_by(id = post_id).first()
# 		comments = DBsession.query(Comment).filter_by(parent_id = post.id)


@app.route('/home/<name>')
def home(name):


@app.route('/canvas/user/<name>')


def canvas(name):
	return render_template('canvas.html', name=name)


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
@app.route('home/uploads/<name>')
def upload:
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(url_for('upload'))


		file=request.files['file']
		if file.filename=='':
			flash('No selected file')
			return redirect(url_for('upload'))
		if file(file.filename):
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		file=Gallery
		return redirect(url_for('home'),filename=filename)

	return render_template('upload.html')



if __name__ == '__main__':
	app.run(debug=True)
