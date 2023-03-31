# Literally just a Flask API that receives Github webhooks.

## What?
It's a simple flask api that receives and verifies GitHub webhook requests, made with minimal boilerplate.

## Why?
I needed something like this to update a website I was working on since I was tired of ssh'ing into the server and pulling every couple minutes and setting up a cron job (while effective) was kind of silly.
I made this with reusability in mind since I'll probably use this code for a lot of my future projects.

## How?
After receiving the request, the api checks for the presence of the sha256 hash and returns early.

Validating the signature happens in, you guessed it, the `validate_signature()` function. I got that code from a discussion on some forum and modified it to suit this case (originally it checked the sha1 hash which is fairly old-school).
Here's how it works:

```python
def validate_signature():
    # Converts the webhook_key (secret password) from a string to bytes.
    # 'password' -> b'password'
    key = bytes(webhook_key, 'utf-8')
    
    # Encrypts the request body with the webhook_key using the sha256 hashing algorithm and then runs hexdigest on it.
    # b'password' -> hmac.HMAC object -> 11d1554f232954fec2afcecb89be7caa7af10ef6d1b23c538d30fbdcb75006bf
    expected_signature = new(key=key, msg=request.data, digestmod=sha256).hexdigest()
    
    # Parses the signature given with the request.
    # sha256=11d1554f232954fec2afcecb89be7caa7af10ef6d1b23c538d30fbdcb75006bf -> 11d1554f232954fec2afcecb89be7caa7af10ef6d1b23c538d30fbdcb75006bf
    incoming_signature = request.headers.get('X-Hub-Signature-256').split('sha256=')[-1].strip()
    
    # Compares the two signature strings and returns the result.
    # The compare_digest function uses an approach designed to prevent timing analysis by avoiding content-based short circuiting behaviour, making it appropriate for cryptography.
    return compare_digest(incoming_signature, expected_signature) # Bool
    
```

The result is then checked and the code returns early if signatures mismatch (`False`) and sends a response with the error code 500 `Forbidden`
Anything after that will execute only if the signatures match.

Here are some things you can do after verifying the request:

#### Running bash scripts!

###### Running a bash script from a directory:
```python
from subprocess import call

scr = call('./script.sh') # If the script has no shebang then add 'shell=True'
```
###### Running a script with arguments:
```python
from subprocess import check_call

scr = check_call(["./script.ksh", arg1, arg2, arg3], shell=True)
```
###### Reading script contents and running them:
```python
from subprocess import call

with open('sleep.sh', 'rb') as file:
    script = file.read()
scr = call(script, shell=True)
```

#### Running terminal commands!

```python
from os import system

system('echo Test')
```

#### Reciting numbers to infinity!

```python
from os import system

i = 0
while True:
    system(f"echo {i}")
    i += 1
```

## What next?
I will probably add a filter that parses the request body and does different things depending on which branches receive updates.

For my current project I need to update two branches - main and dev - so a filter to distinguish these two is a good idea.

## Why Python?
Since it's the language I know best at the time and this task doesn't exactly require a fast and efficient language.
I'm planning on using this code in the future so at some point I'll probably rewrite it in some other language (maybe Rust??)
but that's far off :)
