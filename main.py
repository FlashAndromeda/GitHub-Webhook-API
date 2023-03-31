from flask import Flask, request, json
from os import environ
from hashlib import sha256
from hmac import new, compare_digest
from subprocess import call

app = Flask(__name__)

@app.route('/gh_webhook', methods=['POST'])
def webhook():
	webhook_key = environ.get('WEBHOOK_KEY')

	if not request.headers['x-hub-signature-256']:
		return "Missing X-Hub-Signature-256!", 500

	if not validate_signature(webhook_key):
		return "Bad Signature!", 500

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

def validate_signature(webhook_key):
	key = bytes(webhook_key, 'utf-8')

	expected_signature = new(key=key, msg=bytes(str(request.json.get('payload')), 'utf-8'),digestmod=sha256).hexdigest()
	print(f"Request data bytes: {bytes(str(request.json.get('payload')), 'utf-8')}")
	print(f"Request data type: {type(request.json.get('payload'))}")
	print(f"expected_signature: {expected_signature}")

	with open('request-data.txt', 'w') as file:
		file.write(str(request.json.get('payload')))

	incoming_signature = request.headers.get('X-Hub-Signature-256').split('sha256=')[-1].strip()
	print(f"incoming_signature: {incoming_signature}")

	result = compare_digest(incoming_signature, expected_signature)

	return result

if __name__ == '__main__':
	app.run()
