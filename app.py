import pyrebase

config = {
	"apiKey": "AIzaSyA02qEvsJmODmJc4rEvEK0TnUBk6WPhRYw",
    "authDomain": "hardhack19-8a5a4.firebaseapp.com",
    "databaseURL": "https://hardhack19-8a5a4.firebaseio.com",
    "projectId": "hardhack19-8a5a4",
    "storageBucket": "hardhack19-8a5a4.appspot.com",
    "messagingSenderId": "30778902511"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

from flask import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def basic():
	if request.method == 'POST':
		name = request.form['name']
		db.child("todo").push(name)
		todo = db.child("todo").get()
		to = todo.val()
		return render_template('home.html', t=to.values())
	return render_template('home.html')

if __name__ == '__main__':
	app.run(debug=True)
