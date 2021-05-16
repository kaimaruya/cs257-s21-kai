'''
Team F's Flask Code
'''

import flask
from flask import render_template, request, url_for
import json
import sys

app = flask.Flask(__name__)

# This line tells the web browser to *not* cache any of the files.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/aboutdata')
def aboutData():
    return render_template('aboutdata.html')

@app.route('/results', methods=['POST', 'GET'])
def searchResult():
    '''
    This method is executed once you submit the simple form. It embeds the form responses
    into a web page.
    '''
    #if request.method == 'POST':
        #result = request.form

        # Here is where you would call one or more database methods with the form data.

    return render_template('sampleresults.html', results=result)

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

