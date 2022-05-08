from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd


SPREADSHEET_ID = "1JLwSL4ziK3z4hpuhEMyw9R8WQpg1r8bMEkEuoMxab34"
RANGE_NAME = "Sheet1"


def get_google_sheet(spreadsheet_id, range_name):
    """ Retrieve sheet data using OAuth credentials and Google Python API. """
    scopes = 'https://www.googleapis.com/auth/spreadsheets'
    # Setup the Sheets API
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('frigg/sheets/client_secret.json', scopes)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    gsheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return gsheet

def loadToGoogleSheets(spreadsheet_id, range_name,Input):
    """ Retrieve sheet data using OAuth credentials and Google Python API. """
    scopes = 'https://www.googleapis.com/auth/spreadsheets'#.readonly'
    # Setup the Sheets API
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', scopes)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_name,valueInputOption='RAW', body=Input).execute()

def gsheet2df(gsheet):
    """ Converts Google sheet data to a Pandas DataFrame.
    Note: This script assumes that your data contains a header file on the first row!
    Also note that the Google API returns 'none' from empty cells - in order for the code
    below to work, you'll need to make sure your sheet doesn't contain empty cells,
    or update the code to account for such instances.
    """
    header = gsheet.get('values', [])[0]   # Assumes first line is header!
    values = gsheet.get('values', [])[1:]  # Everything else is data.
    if not values:
        print('No data found.')
    else:
        all_data = []
        for col_id, col_name in enumerate(header):
            column_data = []
            for row in values:
                column_data.append(row[col_id])
            ds = pd.Series(data=column_data, name=col_name)
            all_data.append(ds)
        df = pd.concat(all_data, axis=1)
        return df

import datetime
now = datetime.datetime.now()

def run():
    gsheet = get_google_sheet(SPREADSHEET_ID, RANGE_NAME)
    df = gsheet2df(gsheet)
    values = [
            [
                now.strftime("%d/%m/%Y"),400,300,200,100,
            ],
        ]

    Body = {
        'values' : values,
        }
    loadToGoogleSheets(SPREADSHEET_ID, RANGE_NAME,Body)
    print('Dataframe size = ', df.shape)
    print(df.head())
