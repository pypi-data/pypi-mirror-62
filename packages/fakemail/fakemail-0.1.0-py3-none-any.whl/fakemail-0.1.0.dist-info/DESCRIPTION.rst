Fakemail : an asynchronous command line email proxy
####################################################

Fakemail is a simple SMTP server that runs as a command line script, relaying
incoming messages to an upstream server, to an HTTP endpoint or to stdout.

Fakemail is useful for testing emails during development: it can rewrite the
envelope-to address on all messages to a single address, ensuring messages cannot be
sent to real users.

Fakemail is useful for processing inbound messages in a web application,
by acting as an SMTP-to-HTTP proxy.

Caution: **Fakemail always runs as an open relay**. Ensure you do not expose fakemail on a public address.



Installation
============

pip install -r requirements.txt


Usage
========

To see an up to date list of command line options, run::

    python fakemail.py --help


Examples
---------

Redirect emails for development:

    python fakemail.py --bind 127.0.0.1:2525 --relay 127.0.0.1:25 --rewrite-to=myaddress@example.org


View emails on stdout::

    python fakemail.py --bind 127.0.0.1:2525 --stdout


Feed emails into an HTTP endpoint (SMTP-to-HTTP)::

    python fakemail.py --bind 127.0.0.1:2525 --relay-url="https://mywebservice.example.org/mail-in"

    python fakemail.py --bind 127.0.0.1:2525 --relay-url="https://user:pass@mywebservice.example.org/mail-in"


Multiple relays are possible: you can relay via SMTP, to an HTTP endpoint,
and log to stdout in a single process. If any one relay fails the mail will be
rejected, even if other relays succeed.


