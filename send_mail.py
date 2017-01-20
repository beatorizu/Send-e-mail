from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib


def get_mail_list_from_file(file_path):
    """
    This function reads a file and returns a list of recipients mail.

    Parameters
    ----------
    file_path: str
        The file_path should contain recipients mail address.
        The mails has to be written in this form: name@example.com

    Returns
    -------
    list
        The recipients list.
    """
    with open(file_path) as recipients_file:
        recipients = recipients_file.readlines()
    return list(map(lambda s: s.strip(), recipients))


def send_mail_single_recipient(fromaddr, toaddr, subject, body, passwd, files, toaddrlist):
    """
    This function mails KML and CSV files.

    Parameters
    ----------
    files: list
    passwd: str
    body: str
    subject: str
    toaddr: str
    fromaddr: str
    toaddrlist: list

    Returns
    -------
    None
    """
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = ', '.join(toaddrlist)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    for file in files:
        attachment = open(file, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % file.split('/')[-1])

        msg.attach(part)

        attachment.close()

    # to send
    mailer = smtplib.SMTP('smtp.gmail.com', 587)
    mailer.ehlo()
    mailer.starttls()
    # mailer.connect()
    mailer.login(fromaddr, passwd)

    mailer.sendmail(fromaddr, toaddr, msg.as_string())
    mailer.close()


def send_mail_multiple_recipients(fromaddr, toaddrlist, subject, body, passwd, files):
    """
    This function mails KML and CSV files.

    Parameters
    ----------
    files: list
    passwd: str
    body: str
    subject: str
    toaddrlist: list
    fromaddr: str

    Returns
    -------
    None
    """
    for toaddr in toaddrlist:
        send_mail_single_recipient(fromaddr, toaddr, subject, body, passwd, files, toaddrlist)
