#!/usr/bin/python3
from bottle import post, get, run, request, static_file, redirect, auth_basic, HTTPError, response, route
from .send_mail import send_mail, is_valid_email, AuthenticationException
import os
import sys
import shutil
from pprint import pprint
from .convert import convert, conversions
import json

APPLICATION = 'PrintAtHPI'
HERE = os.path.dirname(__file__) or os.getcwd()
STATIC_BASE_PATH = os.path.join(HERE, "static")
ZIP_PATH = "/" + APPLICATION + ".zip"
REALM = "HPI E-Mail & Passwort (z.B. Max.Mustermann@hpi.de oder Inge.Musterstudent@student.hpi.de)"
NOT_AUTHENTICATED = "Could not authenticate."
SEND_MAILS = True # set this to True/False if you want/ do not want to send emails
DEFAULT_HOST_URL = "https://printathpi.quelltext.eu"

@get('/static/<path:path>')
def get_static_file(path):
    return static_file(path, root=STATIC_BASE_PATH)


def check_hpi_credentials(user, password):
    return is_valid_email(user)

def enable_cors(fn):
    # from https://stackoverflow.com/a/17262900
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, authorization'

        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors
    

def pleaseAuthenticate():
    err = HTTPError(401, NOT_AUTHENTICATED)
    err.headers['WWW-Authenticate'] = 'Basic realm="{}"'.format(REALM)
    err.headers['Access-Control-Allow-Origin'] = '*'
    err.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    err.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, authorization'
    return err


@route('/print', method=['OPTIONS', 'POST'])
@enable_cors
def print_files():
    if not request.auth:
        return pleaseAuthenticate()
    files = {file.filename + ".pdf": convert(file.filename, file.file.read())
             for file in request.files.getlist("files[]")}
    username, password = request.auth
    try:
        if SEND_MAILS:
            send_mail(files, username, password)
    except AuthenticationException:
      return pleaseAuthenticate()
    return "Folgende Dateien wurden{} gesendet: {}".format(" NICHT" * (not SEND_MAILS), ", ".join(files))

@route('/topdf', method=['OPTIONS', 'POST'])
@enable_cors
def route_convert_to_pdf():
    file = request.files.getlist("files[]")[0]
    response.headers["Content-Type"] = "application/pdf"
    response.headers["content-disposition"] ="attachment; filename=\"" + file.filename +"\""
    content = file.file.read()
    result = convert(file.filename, content)
    assert result != content or file.filename.lower().endswith(".pdf")
    return result


@get('/source')
def get_source_redirect():
    """Download the source of this application."""
    redirect(ZIP_PATH)


@get('/printathpi.js')
def printathpi_js():
    """Return the source of the print file."""
    redirect("/static/printathpi.js")

@get('/')
def get_source_redirect():
    """Download the source of this application."""
    redirect("/static/index.html")


@get(ZIP_PATH)
def get_source():
    """Download the source of this application."""
    # from http://stackoverflow.com/questions/458436/adding-folders-to-a-zip-file-using-python#6511788
    path = shutil.make_archive("/tmp/" + APPLICATION, "zip", HERE)
    return static_file(path, root="/")

if __name__ == "__main__":
    print("Conversions to PDF: {}".format(", ".join(list(sorted(conversions.keys())))))
    run(host='', port=8001, debug=True, reload=True)
