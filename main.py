from flask import Flask, request
from os import environ, getenv
from hashlib import sha256
from hmac import new, compare_digest
from subprocess import call
from dotenv import load_dotenv

app = Flask(__name__)
try:
	webhook_key = environ.get('WEBHOOK_KEY')
except KeyError:
	load_dotenv()
	webhook_key = getenv('WEBHOOK_KEY')

@app.route('/gh_webhook', methods=['POST'])
def webhook():
	if not request.headers['x-hub-signature-256']:
		return "Missing X-Hub-Signature-256!", 500

	if not validate_signature():
		return "Bad Signature!", 500

	return "Correct!", 200
	# branch = json.loads((request.data).decode("utf-8")).get('ref').split('/')[-1]
	#
	# if branch == 'dev':
	# 	call('(cd /home/cgi/www-test/ && git pull origin dev)')
	# 	return "Updated dev branch in '/home/cgi/www-test/'", 200
	#
	# elif branch == 'main':
	# 	call('cd /home/cgi/www/ && git pull origin main')
	# 	return "Updated main branch in '/home/cgi/www/'", 200
	#
	# else:
	# 	return f"Cannot find local branch corresponding to {branch} :(", 404

def validate_signature():
	key = bytes(webhook_key, 'utf-8')
	print(key)
	print(request.data)
	expected_signature = new(key=key, msg=request.data, digestmod=sha256).hexdigest()
	print(expected_signature)

	incoming_signature = request.headers.get('X-Hub-Signature-256').split('sha256=')[-1].strip()
	print(incoming_signature)

	return compare_digest(incoming_signature, expected_signature)

if __name__ == '__main__':
	app.run()
