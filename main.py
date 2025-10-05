from flask import Flask, request
import os
import requests
import time
app = Flask(__name__)

@app.route('/')

def main():
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
	checkact = '&action=isPass'
	err = ''
	token = request.args.get('token')
	retry = request.args.get('retry')

	try:
		if retry:
			urlcheck = baseurl + mfacom + token + checkact
			checkOk = getCheck(urlcheck)
			if checkOk is None:
				token = None
				retry = None
		if not retry:
			loops = 2
			for attempt in range(loops):
				if not token:
					if not num:
						err += 'no-num-param. '
					if not pas:
						err += 'no-pas-param. '
					if err:
						print (err.strip())
						return ''
					urllogin = baseurl + logincom + numurl + pasurl
					token = getToken(urllogin)
				if token:
					urlcheck = baseurl + mfacom + token + checkact
					checkOk = getCheck(urlcheck)
					if checkOk is None:
						token = None
						continue
					if checkOk:
						print ('{token}')
						return token
				break
			if not mfaid:
				print ('no-mfaid-param.')
				return ''
			urlsend = baseurl + mfacom + token + sendact
			oksend = getSend(urlsend)
			if not oksend:
				return ''
		code = getCode()
		if not code:
			print ('CODE-NOT-YET-RECEIVED:{token}')
			return f'CODE-NOT-YET-RECEIVED:{token}'
		urlvalid = baseurl + mfacom + token + validact + code
		okvalid = getValid(urlvalid)
		if okvalid == 'VALID':
			print ('{toke}')
			return token
		print ('UNVERIFIED-TOKEN:{token}')
		return f'UNVERIFIED-TOKEN:{token}'
	except:
		return ''

def getToken(urllogin):
	try:
		reslogin = requests.get(urllogin)
		datlogin = reslogin.json()
		token = datlogin.get('token')
		return token
	except:
		return False

def getCheck(urlcheck):
	try:
		rescheck = requests.get(urlcheck)
		datcheck = rescheck.json()
		okcheck = datcheck.get('isPassInThisSession')
		return okcheck
	except:
		return None

def getSend(urlsend):
	try:
		ressend = requests.get(urlsend)
		datsend = ressend.json()
		oksend = datsend.get('message')
		if oksend == 'the code send. please valid the code':
			return True
		return False
	except:
		return False

def getCode():
	gasurl = os.getenv('GASURL')
	timeout = 25
	start = time.time()
	while time.time() - start < timeout:
		try:
			rescode = requests.get(gasurl)
			code = rescode.text.strip()
			if code.isdigit() and len(code) == 6:
				return code
		except:
			continue
		time.sleep(1)	
	return False

def getValid(urlvalid):
	try:
		resvalid = requests.get(urlvalid)
		datvalid = resvalid.json()
		okvalid = datvalid.get('mfa_valid_status')
		return okvalid
	except:
		return False
