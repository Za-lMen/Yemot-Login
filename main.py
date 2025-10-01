from flask import Flask, request
import os
import requests
import time
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
			print("urlsend ", urlsend)

			try:
				ressend = requests.get(urlsend)
				print("ressend ", ressend.text)
				datsend = ressend.json()
				print("datsend ", datsend)
				oksend = datsend.get('message')
				print("oksend ", oksend)

				if oksend == 'the code send. please valid the code':

					try:
                                                
						code = mfaCode()

						if code:

							urlvalid = baseurl + mfacom + token + validact + code

							try:
								resvalid = requests.get(urlvalid)
								datvalid = resvalid.json()
								okvalid = datvalid.get('mfa_valid_status')

								if okvalid == 'VALID':

									return token

								return 'No Valid Received'

							except:
								return 'no valid received'

						return 'No Code Received'

					except:
						return 'no code received'

				return 'No Send Received'

			except:
				return 'no send received'

		return 'No Token Received'

	except:
		return 'no token received'

def mfaCode():
    url = 'https://script.google.com/macros/s/AKfycbyXAdhSDGbcIDxhYH1A3s6biIdiliYeb-cVaM_hbI86JV8wVEMd5jGV-w7GvSJYNciRJg/exec'
    timeout = 90
    start = time.time()
    
    while time.time() - start < timeout:
        
        try:
            
            rescode = requests.get(url)
            code = rescode.text.strip()
            
            if code.isdigit() and len(code) == 6:
                
                return code

        except:
            continue
        
        time.sleep(5)
                        
    return
