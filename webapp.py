from flask import Flask, render_template, request, redirect, url_for, session
from wtforms import *
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import hashlib
import os
from sqlalchemy import update


from database import Base,User,Gallery
from sqlalchemy import create_engine




from database import Base,User
from sqlalchemy import create_engine
engine=create_engine('sqlite:///Webpage.db')
Base.metadata.create_all(engine)
DBSessionMaker=sessionmaker(bind=engine)
DBsession=DBSessionMaker()


current_directory = os.getcwd()
UPLOAD_FOLDER = os.path.join(current_directory, 'static/uploads')
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
    return redirect(url_for('login'))

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



@app.route('/profile')
def profile():
  name = session['username']
  user = DBsession.query(User).filter_by(username = name).first()
  if user == None:
    return render_template('404.html')
  else:
    posts = DBsession.query(Gallery).filter_by(user_id = user.id).all()
    for post in posts:
        print("User:" + post.author.username)
    return render_template('profile.html', posts = posts,user=user)


@app.route ('/chat')
def chat():
	return render_template('chat.html')

@app.route('/home/religion')
def religion():
  return render_template('religion.html')

@app.route ('/about')
def about():
  return render_template('about.html')

@app.route ('/activeabout')
def activeabout():
  return render_template('activeabout.html')

@app.route ('/contact')
def contact():
  return render_template('contact.html')


'''
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
'''



@app.route('/uploads')



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
      gallery = Gallery(user_id = user.id, file_name = "uploads/" + filename, description = request.form['description'], likes = 0)
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

@app.route('/picture_feed_home_like/<int:id>')
def increment_home(id):
    x = DBsession.query(Gallery).filter_by(id = id).first()
    x.likes = x.likes + 1
    DBsession.commit()
    return redirect(url_for('home'))

@app.route('/picture_feed_profile_like/<int:id>')
def increment_profile(id):
    x = DBsession.query(Gallery).filter_by(id = id).first()
    x.likes = x.likes + 1
    DBsession.commit()
    return redirect(url_for('profile'))

if __name__ == '__main__':
  app.run(host = ("0.0.0.0"), debug=True)
