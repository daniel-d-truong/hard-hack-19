#MUST make sure to "export FLASK_APP={file_name}" in terminal before running "flask run"
#use "export FLASK_DEBUG=1" in order to turn on debug mode (automatic update from code)
# Sources of Help: https://www.youtube.com/watch?v=QnDWIZuWYW0&m=19

from flask import Flask, render_template
app = Flask(__name__) #__name__ just means the name of module in python

updates = [
  {
    'author': 'Antony Nguyen',
    'title': 'This Project Sucks',
    'content': 'Good riddance, I\'m being toxic. ',
    'date_posted': '10/31/18'
  },
  {
    'author': 'William Martino',
    'title': 'Butt Plugs Rule!',
    'content': 'Can we please just make a butt plug. ',
    'date_posted': '11/01/18'
  },

]

@app.route("/") #pathway of url
@app.route("/home")
def home():
    return render_template('home.html', updates = updates) #var is same name as var in html

@app.route("/about") #pathway of url
def about():
    return render_template('about.html', title = "About")

#allows app to run & turns debug mode on using Python (w/o bash)
#__main__ is the name of the main module that runs (kinda like main method in Java)
if __name__ == '__main__':
    app.run(debug=True)
