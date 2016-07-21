from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def entry():
	return render_template('entry.html')

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