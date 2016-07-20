from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def entry():
	return render_template('entry.html')

@app.route('/signup')
def signup():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/user/<name>')
def profile(name):
	return render_template('profile.html', name = name)

if __name__ == '__main__':
	app.run(debug=True)