from __future__ import print_function

import os.path
from os import remove

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError

from tkinter import *

import base64

creds = None            # populated for making API calls
root = Tk()             # root node for our tkinter app
max_email_history = 10  # number of recent emails to grab
current_email = 0       # index for current email

# main label node that displays the current email text
main_label = Label(root, font=("Nueva Std Cond", 16),
                   bg="#37566C", fg="#F0F0F0")


def init():
    """
    Initialize values for the app
    """

    root.title("HELLO JOLEEN")
    root.attributes("-fullscreen", True)
    root.bind("<FocusIn>", lambda e: update_app())
    root.config(cursor="none")
    main_label.place(x=0, y=0, relheight=1.0, relwidth=1.0)
    main_label.bind("<Button-1>", lambda e: handle_tap(e))


def handle_tap(e):
    """
    Increment/decrement which email to display based on if the user tapped left or right
    """
    global current_email
    global max_email_history

    # The tap location relative to the % screen width
    relative_tap = e.x / root.winfo_width()

    # increment which email to display if the tap is in the left 50% of the screen
    if relative_tap < 0.5 and current_email < max_email_history:
        current_email = current_email + 1
        update_app()
    # decrement email if tap is in the right 50% of the screen
    elif relative_tap > 0.5 and current_email > 0:
        current_email = current_email - 1
        update_app()


def update_app():
    """
    Call the gmail API and update the main Label with the body of the specified email
    """
    global current_email
    global max_email_history

    # Tell the app to refresh the emails after 250 minutes
    root.after(15000000, update_app)

    # Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    # Can't proceed if there are no labels
    if not labels:
        print('No labels found.')
        return

    # request a list of the specified number of messages
    result = service.users().messages().list(
        userId='me', maxResults=max_email_history).execute()

    # list of dictionaries, where each contains a message ID
    messages = result.get('messages')

    # If there were no emails, don't bother proceeding
    if not messages or len(messages) == 0:
        print('No messages found.')
        return

    # the current message
    msg = messages[current_email]

    # get the message from its id
    text = service.users().messages().get(userId='me', id=msg['id']).execute()
    payload = text['payload']
    headers = payload['headers']

    # Grab the email data (which we decode later)
    parts = payload.get('parts')[0]
    data = parts['body']['data']

    # If the email had no text in the body, don't try to extract the data
    if not data:
        print('No body text found for email ' + current_email)
        return

    # Since the body of the message is encrypted, decode the data with a base 64 decoder
    data = data.replace("-", "+").replace("_", "/")
    decoded_data = str(base64.b64decode(data), 'utf-8')

    # Configure the text in the main Label with the decoded email body
    main_label.config(text=decoded_data)


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """

    # Initialize certain aspects of the GUI
    init()

    # Delete the file token.json if you change these scopes
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    global creds
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                remove('token.json')
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Update the GUI and run the main app loop
    update_app()
    root.mainloop()


if __name__ == '__main__':
    main()
