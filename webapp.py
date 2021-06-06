'''
Team F's Flask Code
'''

import flask
from flask import render_template, request, url_for
import json
import sys
from datasource import DataSource

app = flask.Flask(__name__)

# This line tells the web browser to *not* cache any of the files.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/homepage')
def home2():
    return render_template('homepage.html')

@app.route('/aboutdata')
def aboutData():
    return render_template('aboutdata.html')

@app.route('/sampleresults', methods=['POST', 'GET'])
def searchResult():
    '''
    This method is executed when the form on the main page is submitted. It will either call the createGraph method in datasource.py and return a graph, or provide a warning message.
    '''
    if request.method == 'POST':
        result = request.form
        if result["xvar"] == "None" and result["yvar"] == "None":
            return render_template('homepage.html', error_message = "True")
        data = DataSource()
        data.createGraph(result["xvar"], result["yvar"])
    return render_template('sampleresults.html')


'''
Run the program by typing 'python3 localhost [port]', where [port] is one of 
the port numbers you were sent by my earlier this term.
'''
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)

