from flask import Flask, render_template, request, redirect, url_for, jsonify
import utils
import json
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO
)

app = Flask(__name__)


@app.route('/getTaxon', methods=['GET'])
def load_taxonomy():
    with open(Path("resources", "ebird_taxonomy_v2023.json")) as f:
        taxonomy = json.load(f)
    return jsonify(taxonomy)


@app.route('/getQuizData', methods=['GET'])
def getQuizData():
    quiz_length = int(request.headers["quizLength"])
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month = months.index(request.headers["month"]) + 1
    species_list = json.loads(request.headers["speciesList"])
    quiz_data = utils.quizData(species_list, quiz_length, month)
    sample = [
        {
            "question": "1",
            "species": "Common Loon",
            "mlTag": "612533357"
        },
        {
            "question": "2",
            "species": "Pacific Loon",
            "mlTag": "612491513"
        },
        {
            "question": "3",
            "species": "Red-throated Loon",
            "mlTag": "612519046"
        }
    ]
    return jsonify(quiz_data)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/quiz')
def quiz():
    question = request.args.get('question')
    return render_template('quiz.html')


@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True, host='100.96.209.43')
