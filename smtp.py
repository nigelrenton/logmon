#!/usr/bin/env python3

from configparser import ConfigParser as cp
from smtplib import SMTP as SMTPLIB
from email.message import EmailMessage as em

class Email:
    def __init__(self, subject, body, recipient):
        self.config = cp()
        self.config.read('./config')
        self.subject = subject
        self.body = body
        self.recipient = recipient
        self.server = self.__server()
        self.email = self.__message()
    def __message(self):
        msg = em()
        msg['Subject'] = self.subject
        msg['From'] = self.config['smtp']['from']
        msg['To'] = self.recipient
        msg.set_content(self.body, subtype='html')
        return msg
    def __server(self):
        server = SMTPLIB(
            self.config['smtp']['server'],
            self.config['smtp']['port']
        )
        if self.config['smtp']['ehlo']:
            server.ehlo()
        if self.config['smtp']['starttls']:
            server.starttls()
        server.login(
            self.config['smtp']['user'],
            self.config['smtp']['password']
        )
        return server
    def __send(self):
        send = self.server.send_message(self.email)
        self.server.quit()
        return send
    def send(self):
        return self.__send()


class logmonEmail:
    def __init__(self, job, line):
        self.job = job
        self.line = line
        self.subject = self.__subject()
        self.email = self.__email()
    def __subject(self):
        return 'logmon condition matched in {}'.format(self.job['log'])
    def __header(self):
        return """
        <!DOCTYPE html>
        <head>
        </head>
        """
    def __footer(self):
        return """
        <div>logmon</div>
        """
    def __body(self):
        return """
        <div>
            <p>logmon has matched conditions:<br>
            {conditions}<br>
            in {file}:</p>
            <p>{line}</p>
        </div>
        """.format(
            conditions = ", ".join(self.job['conditions']),
            file = self.job['log'],
            line = self.line
        )
    def __email(self):
        return """
            {header}
            {body}
            {footer}
        """.format(header=self.__header(),body=self.__body(),footer=self.__footer())

          
