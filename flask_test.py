#MUST make sure to "export FLASK_APP={file_name}" in terminal before running "flask run"
#use "export FLASK_DEBUG=1" in order to turn on debug mode (automatic update from code)
# Sources of Help: https://www.youtube.com/watch?v=QnDWIZuWYW0&m=19

from flask import Flask, render_template
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from google.cloud import storage
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import io
import google
import json
import random

app = Flask(__name__) #__name__ just means the name of module in python
#firebase authentication
firebase_admin.initialize_app()
firebase = firebase.FirebaseApplication('https://hard-hack-19-229121.firebaseio.com/', None)
result = firebase.get('/anger', None)
print (result[0])

EMOTIONLESS = '/emotionless'
SURPRISE = '/surprise'
JOY = '/joy'
SORROWFUL = '/sorrowful'
ANGER = '/anger'
# array of emotions
emotions = [EMOTIONLESS, SURPRISE, JOY, SORROWFUL, ANGER]


def detect_faces(uri):
    """Detects faces in images"""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    # image = vision.types.Image()
    # image.source.image_uri = uri
    print (uri)
    with io.open(uri, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    print ('Faces:')
    for face in faces:
        # finds value for likelihood of each emotion
        emotionless_val = likelihood_name[2]
        anger_val = likelihood_name[face.anger_likelihood]
        joy_val = likelihood_name[face.joy_likelihood]
        surprise_val = likelihood_name[face.surprise_likelihood]
        sorrow_val = likelihood_name[face.sorrow_likelihood]
        # likelihood values array
        emotion_vals = [anger_val, joy_val, surprise_val, sorrow_val]

        max = 0
        final_emotion = emotions[max]

        # if one emotion is more likely, it is set to final_emotion
        for x in range(1, 4):
            if likelihood_name.index(emotion_vals[x]) > likelihood_name.index(emotion_vals[max]):
                final_emotion = emotions[x]
                max = x
        result = firebase.get(final_emotion, None)
        random_index = random.randint(0,8)
        print (final_emotion+ " | Index: " + str(random_index))
        return result[random_index]

testPath = "images/canada-head.jpg"


#for i in range(20):
    #detect_faces("william-test/"+str(i)+".bmp")

@app.route("/") #pathway of url
@app.route("/home")
def home():
    return render_template('home.html', url=detect_faces(testPath)) #var is same name as var in html


# @app.route("/about") #pathway of url
# def about():
#     return render_template('about.html', title = "About")

#allows app to run & turns debug mode on using Python (w/o bash)
#__main__ is the name of the main module that runs (kinda like main method in Java)
if __name__ == '__main__':
    app.run(debug=True)
