#
# Send an E-Mail
# from https://docs.python.org/2/library/email-examples.html
#
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import urlencode
from html import escape as html_escape
from os.path import basename
from email.mime.application import MIMEApplication
import re

SUBJECT = "Print at HPI"
TO_MAIL = "Mobile Print HPI <mobileprint@hpi.uni-potsdam.de>"
REPO = "https://github.com/niccokunzmann/printathpi"
PROGRAM_DESCRIPTION = "Print Documents at the Hasso-Plattner-Institute. " + REPO
VALID_DOMAINS = ["hpi.de", "student.hpi.de", "hpi.uni-potsdam.de", "student.hpi.uni-potsdam.de"]

def is_valid_username(name):
    """Check whether this is a valid HPI username."""
    return bool(re.match(r"^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)?$", name))

def is_valid_email(email):
    """Check whether the email addess is valid and from HPI."""
    split = email.split("@")
    if len(split) != 2:
        return False
    name, domain = split
    if domain not in VALID_DOMAINS:
        return False
    return is_valid_username(name)
    
assert not is_valid_email("")
assert not is_valid_email("aasd@123123@")
assert is_valid_email("asd.asd@hpi.de")
assert is_valid_email("asd.asd2@hpi.de")
assert is_valid_email("Asd.asd@hpi.uni-potsdam.de")
assert is_valid_email("Asd.asd@student.hpi.de")
assert is_valid_email("aasd@hpi.de")
assert is_valid_username("Admin")
assert is_valid_username("Nicco.Kunzmann")
assert is_valid_username("Stefan2.sad")
assert not is_valid_username("Stefan2.sad ")
assert not is_valid_username("...")

def send_mail(files, from_mail, password, to=TO_MAIL):
    """
    
    :param dict files: a dict mapping file name (string) to file content (bytes)
    :param str from_mail: the username of a gmail account
    :param str password: the password to the username
    """

    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT
    msg['From'] = from_mail
    msg['To'] = to
    msg['Cc'] = to
    msg['User-Agent'] = __name__ + " " + REPO
    msg.preamble = PROGRAM_DESCRIPTION

    html = """
    <html>
      <head></head>
      <body>
        <p>
          Hi!<br>
          Dies ist eine Nachricht von <a href="{repo}">print at HPI</a> an
          {to_mail}, um
          {filenames} auszudrucken.
        </p>
      </body>
    </html>
    """.format(repo=REPO, to_mail=to, filenames=", ".join(files or ["nichts"]))
    msg_html = MIMEText(html, 'html')
    msg.attach(msg_html)
    
    for name, content in files.items():
        name = basename(name)
        # from https://stackoverflow.com/a/3363254
        part = MIMEApplication(
            content,
            Name=name
        )
        part['Content-Disposition'] = 'attachment; filename="{}"'.format(name)
        msg.attach(part)

    # Send the email via our own SMTP server.
    # with gmail, see
    #   https://www.nixtutor.com/linux/send-mail-through-gmail-with-python/
    s = smtplib.SMTP('owa.hpi.de:587')
    s.starttls()
    username = from_mail.split("@")[0]
    s.login(username, password)
    s.sendmail(from_mail, to, msg.as_string())
    s.quit()
