from flask import Flask, request
import os
app = Flask(__name__)

@app.route('/')

def login():
    num = request.args.get('num', 'No num param')
    pas = request.args.get('pas', 'No pas param')
    mfaid = request.args.get('mfaid', 'No mfaid param')
    baseurl = 'https://www.call2all.co.il/ym/api/'
    loginurl = 'Login'
    numurl = f'username={num}'
    pasurl = f'password={pas}'
    return f'{baseurl}{loginurl}?{numurl}&{pasurl}'
