from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from googleapiclient.errors import HttpError
import base64
import mimetypes

import sqlite3
import pandas as pd
from pandas import DataFrame
import datetime
from getFromDatabase import getEmail

SCOPES = ['https://mail.google.com/']

def sendEmail(to, roomName, emailType, startTime, endTime, date):
    print(emailType)
    print("sendEmail")
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])
    sender = "uninotificationserviceemail@gmail.com"
    if emailType == 'booking':
        subject = "Room booking cancelled"
        message_text = "The room booking for " + roomName + " between " + startTime + " and " + endTime + " on the " + date + " was cancelled"
    else:
        subject = "Watched Room now available"
        message_text = roomName + " is now available between " + startTime + " and " + endTime + " on the " + date
    message = create_message(sender, to, subject, message_text)
    send_message(service,'me',message)

def create_message(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def send_message(service, user_id, message):
  try:
    message = (service.users().messages().send(userId=user_id, body=message).execute())
    print('Message Id: %s' % message['id'])
    return message
  except HttpError as error:
    print('An error occurred: %s' % error)
