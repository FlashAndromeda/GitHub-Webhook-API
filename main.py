from hashlib import sha256
from hmac import new, compare_digest
from os import environ

from flask import Flask, request

api = Flask(__name__)

webhook_key = environ['WEBHOOK_KEY']

@api.route('/gh_webhook', methods=['POST'])
def webhook():
    if not request.headers['x-hub-signature-256']:
        return "Missing X-Hub-Signature-256!", 500

    if not validate_signature():
        return "Bad Signature!", 500

    # Here goes code that executes if the signature is correct!

    return "Success!", 200


def validate_signature():
    key = bytes(webhook_key, 'utf-8')

    expected_signature = new(key=key, msg=request.data, digestmod=sha256).hexdigest()

    incoming_signature = request.headers.get('X-Hub-Signature-256').split('sha256=')[-1].strip()

    return compare_digest(incoming_signature, expected_signature)


if __name__ == '__main__':
    api.run()
