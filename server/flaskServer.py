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
isNormalNW = False

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
	global isNormalNW
	isNormalNW = False
	
	fileName = request.args['file']
	print('======================================================================')
	print(fileName)
	if fileName == 'normal_nw':
		isNormalNW = True
		return 'No Change in nw conditions. Normal.'

	nw.start(fileName)

	ret = 'Network conditions from :{}'.format(fileName)
	return ret

@app.route('/stopNWtrace')
def stopNWtrace():
	global isNormalNW

	if isNormalNW == True:
		isNormalNW = False
		return 'Already normal.'
	return nw.stop()
	# return 'Stopped'


if __name__ == '__main__':
	app.run(host='0.0.0.0')
