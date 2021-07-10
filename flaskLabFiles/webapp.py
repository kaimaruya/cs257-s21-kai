'''
A simple sample web application using Flask. Demonstrates the basics of routes, as well
as how to use forms with Flask.

author: Amy Csizmar Dalal
CS 257, Spring 2021
'''

import flask
from flask import render_template, request
import json
import sys

app = flask.Flask(__name__)

# This line tells the web browser to *not* cache any of the files.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def simpleHome():
    '''
    Simplest example: print something in the browser
    '''
    return 'Hello, and welcome to your first Flask adventure!'

@app.route('/hello')
def inPlaceHome():
    '''
    Demonstration of rendering HTML on the fly, by defining the HTML within the function.
    '''
    htmlStr = '<html lang="en">' + \
    '<head>' + \
    '  <title>Hello</title>' + \
    '</head>' + \
    '<body>' + \
    '  <h1>Hello</h1>' + \
    '  <p>Welcome to your first Flask adventure!</p>' + \
    '</body>' + \
    '</html>'
    return htmlStr

@app.route('/helloAgain')
def templateHome():
    '''
    Demonstration of rendering an HTML template on the fly, with no variables.
    '''
    return render_template('hello.html')

@app.route('/fancyHello')
def fancyHome():
    '''
    Demonstration of rendering an HTML template on the fly, where the HTML template 
    contains a stylesheet and an image
    '''
    return render_template('fancyHello.html')

@app.route('/greet/<person>/')
def greet(person):
    '''
    Demonstration of passing a parameter into a template.
    '''
    return render_template('greet.html',
                           person=person)

@app.route('/bigGreet/', methods=['GET'])
def greetAgain():
    '''
    Demonstration of passing multiple parameters into a template.
    '''
    person = request.args.get('person')
    year = request.args.get('classYear')
    return render_template('biggerGreet.html',
                           person=person, year=year)

@app.route('/form')
def homeWithForm():
    '''
    Demonstration of rendering a simple form.
    '''
    return render_template('index.html')    


@app.route('/results', methods=['POST', 'GET'])
def searchResult():
    '''
    This method is executed once you submit the simple form. It embeds the form responses
    into a web page.
    '''
    if request.method == 'POST':
        result = request.form

        # Here is where you would call one or more database methods with the form data.

    return render_template('result.html', results=result)

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

