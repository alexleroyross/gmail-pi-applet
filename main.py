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

creds = None
root = Tk()
root.title("HELLO")
max_email_history = 10
current_email = 0

def tap_right():
    global current_email
    if current_email > 0:
        current_email = current_email - 1
    call_api()

def tap_left():
    global current_email
    global max_email_history
    if current_email < max_email_history:
        current_email = current_email + 1
    call_api()

def handle_tap(e):
    global current_email
    global max_email_history
    relative_tap = e.x / root.winfo_width()
    if relative_tap < 0.5 and current_email < max_email_history:
        current_email = current_email + 1
        call_api()
    elif relative_tap > 0.5 and current_email > 0:
        current_email = current_email - 1
        call_api()

# frame = Frame(root, bg="pink")
# frame.place()
# frame.pack_propagate(False)

# left_button = Button(root, command=tap_left, bg=None, fg=None)
# right_button = Button(root, command=tap_right, bg="red", fg="red")
main_label = Label(root, font=("Courier", 24), bg="#37566C", fg="#F0F0F0")

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def app_loop():
    root.bind("<FocusIn>", lambda e:call_api())
    # frame.columnconfigure(0, weight=1)
    # frame.rowconfigure(0, weight=1)
    # root.columnconfigure(0, weight=1)
    # root.columnconfigure(1, weight=1)
    # root.rowconfigure(0, weight=1)
    # root.config(cursor="none")
    # main_label.grid(column=0,row=0)
    main_label.place(x=0,y=0,relheight=1.0,relwidth=1.0)
    # left_button.grid(column=0,row=0, sticky="nsew")
    # right_button.grid(column=1,row=0, sticky="nsew")
    # left_button.tkraise()
    # right_button.tkraise()
    main_label.bind("<Button-1>", lambda e:handle_tap(e))

    call_api()
        
    # except:
    #     print("ERROR ERROR NOOOO")

    # TODO: use while True: loop here!!
    root.mainloop()

    # print('Labels:')
    # for label in labels:
    #     print(label['name'])

def call_api():
    global current_email
    global max_email_history

    print("CALLING APIIIIIII")
    # Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
        return
    
    # labels_gfx = []

    # for label in labels:
    #     label_gfx = Label(root, text=label['name'])
    #     label_gfx.pack()
    #     labels_gfx.append(label_gfx)
    

    # request a list of all the messages
    result = service.users().messages().list(userId='me', maxResults=max_email_history).execute()

    # list of dictionaries, where each contains a message ID
    messages = result.get('messages')
  
    # iterate through all the message dictionaries
    # for msg in messages:
    msg = messages[current_email]
    # print("BAG")
    # get the message from its id
    text = service.users().messages().get(userId='me', id=msg['id']).execute()

    # try:
    payload = text['payload']
    headers = payload['headers']

    # Look for subject and sender email in the headers
    for d in headers:
        if d['name'] == 'Subject':
            subject = d['value']
        if d['name'] == 'From':
            sender = d['value']

    # The body of the message is encrypted, so we must decode it.
    # Get the data and decode it with base 64 decoder.
    parts = payload.get('parts')[0]
    data = parts['body']['data']
    data = data.replace("-","+").replace("_","/")
    decoded_data = str(base64.b64decode(data), 'utf-8')

    # Printing the subject, sender's email and message
    print("Subject: ", subject)
    print("From: ", sender)
    print("Message: ", decoded_data)
    print('\n')

    # Label(root, text="Subject: " + subject).pack()
    # Label(root, text="From: " + sender).pack()
    # main_label = Label(root, text=decoded_data, font=("Courier", 56))
    main_label.config(text=decoded_data)


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    root.attributes("-fullscreen", True)

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

    try:
        app_loop()


    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()