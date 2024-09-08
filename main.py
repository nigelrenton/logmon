#!/usr/bin/env python3

import time
import threading
from datetime import datetime
from jobs import jobs
import io
import os.path
from smtp import Email, logmonEmail
import sys

class Process:
    def __init__(self, line, session):
        self.line = line
        self.session = session
    def __parse(self):
        if all(e in self.line for e in self.session.job['conditions']):
            if time.time() - self.session.timectl > self.session.job['no_repeat'] * 60:
                self.session.timectl = time.time()
                for alert in self.session.job['alerts']:
                    match alert:
                        case 'console':
                            print('{} logmon condition matched: {}'.format(datetime.now().isoformat(), self.line))
                        case 'email':
                            for recipient in self.session.job['email_recipients']:
                                self.__send_mail(recipient)
    def __send_mail(self, recipient):
        em = logmonEmail(self.session.job, self.line)
        email = Email(em.subject, em.email, recipient)
        email.send()
    def parse(self):
        self.__parse()

class Session:
    def __init__(self, job):
        self.timectl = 0
        self.job = job
        self.log = io.open(self.job['log'])
    def __monitor(self):
        self.log.seek(0, 2)
        while True:
            line = self.log.readline()
            if line:
                Process(line, self).parse()
            else:
                time.sleep(1)
    def run(self):
        self.__monitor()

class ValidateJob:
    def __init__(self, job):
        self.job = job
        self.__log()
        self.__email()
    def __log(self):
        if not os.path.exists(self.job['log']):
            print('Log {} does not exist for job {}. Check the path'.format(self.job['log'], self.job['id']))
            sys.exit()
    def __email(self):
        if 'email' in self.job['alerts']:
            if len(self.job['email_recipients']) < 1:
                print('No valid email recipients in job {}. Add recipients or remove email as alert type'.format(self.job['id']))
                sys.exit()

def main():
    print('LOGMON STARTED: {}'.format(datetime.now().isoformat()))
    threads = []
    for job in range(len(jobs)):
        jobs[job]['id'] = job
        ValidateJob(jobs[job])
    for job in range(len(jobs)):
        session = Session(jobs[job])
        thread = threading.Thread(target=session.run)
        threads.append(thread)
        thread.start()

def test(n):
    print(n)

if __name__ == "__main__":
    main()
