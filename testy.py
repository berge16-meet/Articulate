from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def uploads():
    posts = [
        {
            'picture': "static/pic.jpg",
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
        }
    ]

    return render_template('profile.html', posts=posts)

if __name__ == '__main__':
	app.run(debug=True)
