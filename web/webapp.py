import flask
from flask import render_template, request
import json
import sys
from datasource import DataSource

app = flask.Flask(__name__)

# This line tells the web browser to *not* cache any of the files.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/aboutData')
def about_data():
    return render_template('abooutdata.html')

@app.route('/graph', methods=['POST', 'GET'])
def get_graph():
    if request.methods == 'POST':
        result = request.form
        datasource = DataSource();
        datasource.plot_data(result)
    return render_template('result.html, results=result')