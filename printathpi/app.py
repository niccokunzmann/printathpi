#!/usr/bin/python3
from bottle import post, get, run, request, static_file, redirect, auth_basic, HTTPError, response
from .send_mail import send_mail, is_valid_email, AuthenticationException
import os
import sys
import shutil
from pprint import pprint
from .convert import convert

APPLICATION = 'PrintAtHPI'
HERE = os.path.dirname(__file__) or os.getcwd()
STATIC_BASE_PATH = os.path.join(HERE, "static")
ZIP_PATH = "/" + APPLICATION + ".zip"
REALM = "HPI E-Mail & Passwort (z.B. Max.Mustermann@hpi.de oder Inge.Musterstudent@student.hpi.de)"
NOT_AUTHENTICATED = "Could not authenticate."
SEND_MAILS = True # set this to True/False if you want/ do not want to send emails

@get('/static/<path:path>')
def get_static_file(path):
    return static_file(path, root=STATIC_BASE_PATH)


def check_hpi_credentials(user, password):
    return is_valid_email(user)

@post('/print')
@auth_basic(check_hpi_credentials, REALM, text=NOT_AUTHENTICATED)
def print_files():
    files = {file.filename + ".pdf": convert(file.filename, file.file.read())
             for file in request.files.getlist("files[]")}
    username, password = request.auth
    try:
        if SEND_MAILS:
            send_mail(files, username, password)
    except AuthenticationException:
        err = HTTPError(401, NOT_AUTHENTICATED)
        err.add_header('WWW-Authenticate', 'Basic realm="{}"'.format(REALM))
        return err
    return "Folgende Dateien wurden{} gesendet: {}".format(" NICHT" * (not SEND_MAILS), ", ".join(files))

@get('/source')
def get_source_redirect():
    """Download the source of this application."""
    redirect(ZIP_PATH)

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
    run(host='', port=8001, debug=True, reload=True)
