import pandas as pd
import base64 
import json
import csv
import datetime
import requests
from urllib.parse import urlencode
import os.path
from os import path
from pprint import pformat

#use client id and secret to generate a token 
cid = 'a073e9a22f0545c4907433898bf177fa'
secret = '63571eb665004e8a8f61f269f53320eb'

#creating SpotifyAPI class to perform authorization and get token
class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"
    
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }
    
    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        } 
    
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
            # return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True
    
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token() 
        return token
    

## NOW STARTING ETL PIPELINE
#accessing json file with personal streaming history from GitHub rep
url = "https://raw.githubusercontent.com/kara-koopman/DS3002-Project-1/main/StreamingHistory0.json"
resp = requests.get(url)
data = json.loads(resp.text)

#loading json file into pandas dataframe to manipulate rows and columns
df = pd.DataFrame(data)
print("Originial Data Frame Size: ")
row = df.shape[0]
col = df.shape[1]
print("Records: "+str(row))
print("Columns: "+str(col))

#we are only interested in the columns "artistName" and "trackName" because these will be used in our API query for the track ID
#using the track ID we can then find the audio features of that track and add it to our track data
#we will also reduce the number rows to minimize the number of API calls we need
df_subset = df.loc[0:50,['artistName','trackName']]

#we will now use the Spotify API to add a column to our subsetted dataframe - using the information stored in the 'artistName' and 'trackName'
#columns we will find the track ID using the search function of the API 

#creating an empty list to store ID values in 
id_list = []

#using API client ID and secret to generate authorization token
spotify = SpotifyAPI(cid,secret)
spotify.perform_auth
token = SpotifyAPI.get_access_token(spotify)
headers = {
    "Authorization": f"Bearer {token}"
}

#iterating through rows of dataframe to pull artist name and track name to search for track ID
#if unable to perform API call, program will raise exception informing user
for index, row in df_subset.iterrows():
    tName = row['trackName']
    aName = row['artistName']
    endpoint = "https://api.spotify.com/v1/search"
    data = f"q=track:'{tName}'%20artist:'{aName}&type=track"
    lookup_url = f"{endpoint}?{data}"
    r = requests.get(lookup_url, headers=headers)
    if r.status_code not in range(200, 299):  
        raise Exception('Unable to perform API call')
    else:
        #adds track ID to id_list 
        case = {'track ID': r.json()['tracks']['items'][0]['id']}
        id_list.append(case)

#now making list into a dataframe so we can concatenating it our existing subsetted list    
id_df = pd.DataFrame(id_list)
updated_table = pd.concat([df_subset, id_df], axis = 1)
print('\n')
print("Modified Data Frame Size:")
row = updated_table.shape[0]
col = updated_table.shape[1]
print("Records: "+str(row))
print("Columns: "+str(col))

savingPath = r'C:\Users\Student\OneDrive - University of Virginia\Desktop\College\Fall 2021\DS 3002'

if path.exists(savingPath):
    fileName = '\Koopman_DS3002_Project.csv'
    try:
        updated_table.to_csv(savingPath+fileName)
    except:
        raise Exception("Could not write updated dataframe to CSV")
else:
    print('File path does not exist - update savingPath variable for saving destination on computer')
