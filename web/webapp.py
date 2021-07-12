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

@app.route('/aboutdata')
def about_data():
    return render_template('aboutdata.html')

@app.route('/graph', methods=['POST', 'GET'])
def get_graph():
    if request.method == 'POST':
        result = request.form
        datasource = DataSource();
        print(result)
        datasource.plot_data(result['firstVariable'], result['secondVariable'])
    return render_template('plot.html')
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)