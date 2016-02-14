#coding:utf-8
import os
import logging
import flask
import util
import sendgrid
import tempfile
import datetime
import urllib2

app = flask.Flask(__name__, instance_relative_config=True)

app.config.from_object('config.default')
app.config.from_pyfile('config.py')

# Logging configuration
stderr_log_handler = logging.StreamHandler()
app.logger.addHandler(stderr_log_handler)
app.logger.setLevel(logging.DEBUG)

sendgrid_key = app.config['sendgrid_key']
local_secret = app.config['local_secret']

@app.route("/", methods=("GET",))
def webhook_get_handler():
    return flask.Response(status=200)


@app.route("/", methods=("POST",))
def webhook_post_handler():
    payload = flask.request.json
    app.logger.info("Received Upload '%s' for FormID: '%s' on '%s'", payload["UniqueID"], payload["FormID"], str(datetime.datetime.now()))

    sg = sendgrid.SendGridClient(sendgrid_key)
    message = sendgrid.Mail()

    message.add_substitution(':name', payload['Name'])
    message.add_substitution(':email', payload['Email'])
    message.add_substitution(':phone', payload['Phone'])
    message.add_substitution(':date', payload['Date'])

    message.add_to('Sagar <sagu1994@gmail.com>')
    message.set_subject('New Form Notification from Python Webhook')
    message.set_html('<!DOCTYPE html><html><body> <table style="width:50%"> <tr> <td>Name</td> <td>:name</td> </tr> <tr> <td>Email</td> <td>:email</td> </tr> <tr> <td>Phone</td> <td>:phone</td> </tr> <tr> <td>Date</td> <td>:date</td> </tr></table> </body></html>')
    message.set_text('New Form received from :name with Email ID :email and Phone :phone on :date. Attachment if any can be found below.')
    message.set_from('Sagar Pate <cleveridiot94@email.com>')
    
    url = str(payload["File Attachment"])

    if url != '':
        file_name = file_name = url.split('/')[-1]
        tmp_file = tempfile.NamedTemporaryFile(suffix=file_name)
        data = urllib2.urlopen(url).read()
        tmp_file.write(data)
        message.add_attachment(file_name, tmp_file.name)
        tmp_file.close()
    
    status, msg = sg.send(message)
    
    return flask.Response(status=200)

@app.before_request
def validate_request_signature():
    if flask.request.method == "GET":
        return

    payload = flask.request.json
    remote_secret = payload["HandshakeKey"]

    if local_secret != remote_secret:
        app.logger.warning("Detected invalid signature, aborting.")
        return flask.Response(status=403)


@app.before_request
def log_request():
    app.logger.debug("Received request: %s %s", flask.request.method, flask.request.url)

@app.before_request
def validate_json_payload():
    if flask.request.method == "GET":
        return
    if flask.request.json is None:
        return flask.Response(status=400)


if __name__ == '__main__':
    app.run(debug=True)
