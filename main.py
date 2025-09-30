from flask import Flask, request
import os
import requests
app = Flask(__name__)

@app.route('/')

def login():
	num = request.args.get('num')
	pas = request.args.get('pas')
	mfaid = request.args.get('mfaid')
	baseurl = 'https://www.call2all.co.il/ym/api/'
	logincom = 'Login?'
	numurl = f'username={num}'
	pasurl = f'&password={pas}'
	mfacom = 'MFASession?token='
	sendact = f'&action=sendMFA&mfaId={mfaid}&mfaSendType=EMAIL'
	validact = '&action=validMFA&mfaCode='
	err = ''

	if not num:
		err += 'no num param. '
	if not pas:
		err += 'no pas param. '
	if not mfaid:
		err += 'no mfaid param.'
	if err:
		return err.strip()

	urllogin = baseurl + logincom + numurl + pasurl
	
	try:
		reslogin = requests.get(urllogin)
		datlogin = reslogin.json()
		token = datlogin.get('token')

		if token:

			urlsend = baseurl + mfacom + token + sendact

			try:
				ressend = requests.get(urlsend)
				datsend = ressend.json()
				oksend = datsend.get('message')

				if oksend == 'the code send. please valid the code':

					urlcode = 'ana-aref nisht'

					try:
						code = requsts.get(urlcode)

						if code:

							urlvalid = baseurl + mfacom + token + validact + code

							try:


								if:

								

							except:
								

						return 'No Code Received'

					except:
						return 'no code received'

				return 'No Send Received'

			except:
				return 'no send received'

		return 'No Token Received'

	except:
		return 'no token received'

