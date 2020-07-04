#!/usr/bin/python
#
# Flask server, woo!
#

from flask import Flask, request, redirect, url_for, send_from_directory
from nw_simulate import nw
# Setup Flask app.
app = Flask(__name__)
app.debug = True
nw = nw()

# Routes
@app.route('/')
def root():
  return 'Welcome to video server'

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)

@app.route('/networkTrace', methods=['GET'])
def startNWtrace():
	
	fileName = request.args['file']
	print('======================================================================')
	print(fileName)
	nw.start(fileName)

	return 'Network conditions from :{}'.format(fileName)

@app.route('/stopNWtrace')
def stopNWtrace():
	nw.stop()
	return 'Stopped'


if __name__ == '__main__':
	app.run(host='0.0.0.0')
