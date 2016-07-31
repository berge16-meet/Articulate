from flask import Flask, render_template, request, redirect, url_for, session
from wtforms import *
from flask_wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import hashlib
import os


from database import Base,User,Gallery
from sqlalchemy import create_engine




from database import Base,User
from sqlalchemy import create_engine
engine=create_engine('sqlite:///Webpage.db')
Base.metadata.create_all(engine)
DBSessionMaker=sessionmaker(bind=engine)
DBsession=DBSessionMaker()

UPLOAD_FOLDER = '/home/student/Articulate/static/uploads'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

#app setup, do not touch
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'OASIUFHASIH087Y*&^(*&^OSIHUFD'

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


@app.route('/')
def entry():
  return render_template('entry.html')


class SignUpForm(Form):
  first_name = StringField("First name:")
  last_name = StringField("Last name:")
  email = StringField("Email:", [validators.Email()])
  username=StringField("Username:",[validators.Required()])
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

  signup_form = SignUpForm(request.form)

  if request.method == 'POST':

    firstname=request.form['first_name']
    lastname=request.form['last_name']
    email=request.form['email']
    password=request.form['password']
    password = hash_password(password)
    gender=request.form['gender']
    nationality=request.form['nationality']
    dob=request.form['date_of_birth']
    biography=request.form['biography']
    username=request.form['username']


    user=User(firstname=firstname, lastname=lastname,email=email, password=password, username= username,gender=gender, nationality=nationality,date=dob,bio=biography)
    DBsession.add(user)
    DBsession.commit()
    return redirect(url_for('profile', name = username))

  else:
    return render_template('signup.html', form = signup_form)




class Loginform(Form):
  email=StringField('Email:',[validators.Required()])
  password=PasswordField('Password:',[validators.required()])
  submit=SubmitField('Submit')



@app.route('/login',methods=['GET','POST'])
def login():

  loginform=Loginform(request.form)

  if request.method == 'GET':

  	return render_template('login.html', form=loginform)

  else:

    email=request.form['email']
    password=request.form['password']

    user_query = DBsession.query(User).filter(User.email.in_([email]), User.password.in_([hash_password(password)]))

    user = user_query.first()

    if user != None:

      session['id'] = user.id
      session['username'] = user.username
      #for logout:
      #del flask.session['uid']
      return redirect(url_for('profile', name = user.username))
    #if the user does not have an account
    else:
      return render_template('login.html',form=loginform)






'''
  loger=DBsession.query(User).filter_by(email=email)
  if DBsession.query(User).filter_by(email=loger.email)!=None:
    if loger.password==DBsession.query(User).filter_by(email=loger.email).password:
      return redirect (url_for('home',name=DBsession.query(User).filter_by(email=loger.email).firstname))
'''

@app.route('/home')
def home():
    posts = DBsession.query(Gallery).all()
    return render_template('home.html', posts = posts)

@app.route('/profile/<name>')
def profile(name):
	user = DBsession.query(User).filter_by(username = name).first()
	if user == None:
		return render_template('404.html')
	else:
		posts = DBsession.query(Gallery).filter_by(user_id = user.id).all()
		return render_template('profile.html', posts = posts,user=user)





@app.route ('/about')
def about():
  return render_template('about.html')

@app.route ('/contact')
def contact():
  return render_template('contact.html')

def valid_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class UploadForm(Form):
  description = TextAreaField("Describe your picture, remember to keep it focused")
  submit = SubmitField("Submit")

#should be ONLY upload link
@app.route('/upload', methods = ['GET', 'POST'])
def upload():

  upload_form = UploadForm()
  if request.method == 'POST' and session.get('id') != None:
    #checks if file was uploaded
    if 'file' not in request.files:
      return redirect(url_for('upload'))

    file = request.files['file']
		#if user submits an empty file, return a the same upload
    if file.filename == '':
      return redirect(url_for('upload', form = upload_form))

    if file and valid_file(file.filename):
      filename = secure_filename(file.filename)
      path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
      file.save(path)
			#finds user
      user = DBsession.query(User).filter_by(id = session['id']).first()
			#creates link to file in the database
      gallery = Gallery(user_id = user.id, file_name = "uploads/" + filename, description = request.form['description'])
      DBsession.add(gallery)
      DBsession.commit()
      return redirect(url_for('profile', name = user.username))

	#if the user is not logged in send him to the log in page
  elif session.get('id') != None:
    return render_template('upload.html', form = upload_form)

	#get request
  else:
    return redirect('login')

@app.route('/canvas')
def canvas():
  return render_template('canvas.html')

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404


if __name__ == '__main__':
  app.run(debug=True)
