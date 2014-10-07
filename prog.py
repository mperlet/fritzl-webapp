 # -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify,\
				  url_for, redirect, flash, request, Response, send_file
import codecs, os, random, json, string, commands
from fritzl.fritzl import Fritzl
from functools import wraps
from config import user, pw, fritzboxpw
 
app = Flask(__name__)
app.secret_key = 'some_secret'


def check_auth(username, password):
    return username == user and password == pw

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
      
@app.route('/')
@requires_auth
def index():
	f.get_sid()
	return render_template('index.html',)

@app.route('/switch', methods=['GET'])
@requires_auth
def switch_dect200():
	status = request.args.get('state')
	device = request.args.get('device')
	dev_id = device.replace('dev', '')
	if status == 'true':
		f.switch_on(dev_id)
	else:
		f.switch_off(dev_id)

	return jsonify({'status': status})

@requires_auth
@app.route('/switch_info', methods=['GET'])
def switch_dect200_info():
	ret_dict = {}
	info = f.get_info()
	names = f.get_device_names()
	for dev in names.keys():
		ret_dict[dev] = {'id': dev,
						 'name': names[dev], 
						 'status': info[dev]}
	return jsonify(ret_dict)

@requires_auth
@app.route('/get_power', methods=['GET'])
def get_power():
	return jsonify(f.get_power())


if __name__ == "__main__":
	f = Fritzl(fritzboxpw)
	app.debug = True
	app.run(host='0.0.0.0')

