from flask import Flask, render_template, request
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'guess who'

db = SQLAlchemy(app)

@app.route('/')
def entry():
	return render_template('entry.html')

class SignForm(Form):
	name = StringField('what is your')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		return redirect(url_for('home'))
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/user/<name>')
def profile(name):
	return render_template('profile.html', name = name)

@app.route('/home/user/<name>')
def home():
	return render_template('home.html', name=name)

@app.route ('/canvas/user/<name>')
def canvas(name):
	return render_template('canvas.html', name=name)
@app.route ('/chat/user/<name>')
def chat(name):
	return render_template('chat.html')






if __name__ == '__main__':
	app.run(debug=True)