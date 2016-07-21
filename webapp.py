<<<<<<< HEAD
from flask import Flask, render_template, request
app = Flask(__name__, static_url_path="", static_folder="static")
=======
from flask import Flask, render_template, request, redirect,url_for
from flask import session as web_session
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
>>>>>>> 7f41e37480ab61bf7fac687237af76796f32ff74

from database import Base,User
from sqlalchemy import create_engine
engine=create_engine('sqlite:///Webpage.db')
Base.metadata.create_all(engine)
DBSession=sessionmaker(bind=engine)
session=DBSession
app.config['SECRET_KEY'] = 'guess who'

db = SQLAlchemy(app)



@app.route('/')
def entry():
	return render_template('entry.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():

	if request.method == 'GET':
		return render_template('signup.html')
	
	
	else: 
		firstname=request.form['firstname']
		print(firstname)
		return redirect(url_for('home',name=firstname))
	

@app.route('/login')
def login():
	return render_template('login.html')

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
