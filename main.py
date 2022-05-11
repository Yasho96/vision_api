from google.cloud import vision
from flask import render_template, Flask, request
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/display',  methods=['GET', 'POST'])
def display():

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_key.json"

    # Imports the Google vision library
    from google.cloud import vision

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Performs label detection on the image file
    response = client.label_detection(
        {
            "source": {
                "image_uri": "gs://piyumi_test_bucket/humans-2.jpeg"
            },
        }
    )
    labels = response.label_annotations

    allDescriptions = []

    for label in labels:
        allDescriptions.append(
            {label.description: str(round(label.score * 100, 2))})

    return render_template("main.html", transcript=allDescriptions)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
