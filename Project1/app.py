import requests
import os
from dotenv import load_dotenv, find_dotenv

AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/artists/3TVXtAsR1Inumwj472S9r4/top-tracks'

load_dotenv(find_dotenv())

auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': os.getenv('CLIENT_ID'),
    'client_secret': os.getenv('CLIENT_SECRET'),
})


auth_response_data = auth_response.json()#make data JSON

access_token = auth_response_data['access_token']#uses access token

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)#Not 100% sure on this line
}

r = requests.get(BASE_URL, 
                headers=headers, 
                params={'market':'US' , 'song': 'name', 'limit': 10})


output = r.json()


for i in range (0,10):
    print(output['tracks'][i]['album']['name'])