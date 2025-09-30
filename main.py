from flask import Flask, request
import os
app = Flask(__name__)

@app.route('/')

def login():
    num = request.args.get('num')
    pas = request.args.get('pas')
    mfaid = request.args.get('mfaid')
    baseurl = 'https://www.call2all.co.il/ym/api/'
    logincon = 'Login'
    numurl = f'username={num}'
    pasurl = f'password={pas}'
    err = ''

    if not num:
        err += 'no num param. '

    if not pas:
        err += 'no pas param. '

    if not mfaid:
        err  += 'no mfaid param.'

    if err:
        return err.strip()

    urllogin = f'{baseurl}{logincon}?{numurl}&{pasurl}'
    try:
        reslogin = requests.get(urllogin)
        datlogin = reslogin.json()
        token = datlogin.get('token')
        if token:
            return token
        return 'No Token Received'

    except:
        return 'no token received'

