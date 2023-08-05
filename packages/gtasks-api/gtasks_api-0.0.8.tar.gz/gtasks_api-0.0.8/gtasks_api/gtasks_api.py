from __future__ import print_function

import os.path
import pickle

import httplib2
from google.auth.transport.requests import Request

import googleapiclient._auth
import googleapiclient.http
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/tasks.readonly' , 'https://www.googleapis.com/auth/tasks']


class GtasksAPI(object):


    def __init__(self, credentials_json, token_pickle):
        self._creds = None
        self.service = None
        self._flow = None
        self._credentials_json = credentials_json
        self._token_pickle = token_pickle
        self.auth_url = ""
        self._connect()

    def _build_request(self, http, *args, **kwargs):
        new_http = googleapiclient._auth.authorized_http(self._creds)
        return googleapiclient.http.HttpRequest(new_http, *args, **kwargs)

    def _connect(self):
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization self._flow completes for the first
        # time.
        if os.path.exists(self._token_pickle):
            with open(self._token_pickle, 'rb') as token:
                self._creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self._creds or not self._creds.valid:
            if self._creds and self._creds.expired and self._creds.refresh_token:
                self._creds.refresh(Request())
            else:
                self._flow = InstalledAppFlow.from_client_secrets_file(self._credentials_json, SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
                self.auth_url, _ = self._flow.authorization_url(prompt='consent')
                print('Visit this url to finish authentication : {}'.format(self.auth_url))
                return
        self.service = build('tasks', 'v1', credentials=self._creds, requestBuilder=self._build_request)

    def finish_login(self, auth_code: str):
        self._flow.fetch_token(code=auth_code)
        self._creds = self._flow.credentials
        self.service = build('tasks', 'v1', credentials=self._creds, requestBuilder=self._build_request)
        # Save the credentials for the next run
        with open(self._token_pickle, 'wb') as token:
            pickle.dump(self._creds, token)

    def get_taskslist_id(self, list_name: str):
        try:
            all_list = self.service.tasklists().list().execute()    
            if not all_list['items']:
                return
            else:
                for task_list in all_list['items']:
                    if task_list['title'] == list_name:
                        return task_list['id']
        except Exception as e:
            raise e
            return

    def get_task_id(self, list_id: str, task_name: str):
        try:
            tasks_list = self.service.tasks().list(tasklist = list_id).execute()    
            if not tasks_list['items']:
                return
            else:
                for task in tasks_list['items']:
                    if task['title'] == task_name:
                        return task['id']
        except Exception as e:
            raise e
            return
