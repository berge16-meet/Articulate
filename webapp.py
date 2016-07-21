from flask import Flask, render_template, request
app = Flask(__name__, static_url_path="", static_folder="static")
from flask import Flask, render_template, request, redirect,url_for
from flask import session as web_session
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

from database import Base,User
from sqlalchemy import create_engine
engine=create_engine('sqlite:///Webpage.db')
Base.metadata.create_all(engine)
DBSession=sessionmaker(bind=engine)
session=DBSession
app.config['SECRET_KEY'] = 'guess who'

db = SQLAlchemy(app)

user1=User(firstname='berge', lastname='benamram',email='berge@gmail.com',username='bergi',password='123',interests='art',nationality='palestinian',gender='male',dob='1',mob='2',yob='1999',bio='strong',pic='https://www.google.co.il/search?q=bear&client=ubuntu&hs=PdF&channel=fs&tbm=isch&imgil=jcrrgtQvtl8FOM%253A%253Bi2dpMZFmYqIQkM%253Bhttp%25253A%25252F%25252Fwww.urbandictionary.com%25252Fdefine.php%25253Fterm%2525253Dbear&source=iu&pf=m&fir=jcrrgtQvtl8FOM%253A%252Ci2dpMZFmYqIQkM%252C_&usg=__BVyho6vwaIY0oDDAfN_l-YGBvM0%3D&biw=1301&bih=671&ved=0ahUKEwidzM22yoTOAhUHuBQKHTtrBZQQyjcImQE&ei=OMOQV53QGIfwUrvWlaAJ#imgrc=jcrrgtQvtl8FOM%3A')

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
