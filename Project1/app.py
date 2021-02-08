import requests
import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template 

app = Flask(__name__)

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
                params={'market':'US'})


output = r.json()


print(output['tracks'][0]['album']['name'])
print(output['tracks'][0]['artists'][0]['name'])
print(output['tracks'][0]['album']['images'][0]['url'])

song =(output['tracks'][0]['album']['name'])
artist =(output['tracks'][0]['artists'][0]['name'])
cover = (output['tracks'][0]['album']['images'][0]['url'])


# HTML BELOW [][][][][] HTML BELOW [][][][][] HTML BELOW [][][][][] HTML BELOW [][][][][] HTML BELOW [][][][][] HTML BELOW [][][][][] HTML BELOW [][][][][] HTML BELOW [][][][][] HTML BELOW [][][][][]




#blah =["https://i.scdn.co/image/ab67616d0000b27352c75ed37313b889447011ef"]

@app.route('/')
def spotifyAPI():
    print('HTML IN PROGRESS')
    
    return render_template(
        "indexs.html",
        songlen=len(song),
        song=song,
        artistlen=len(artist),
        artist=artist,
        coverlen=len(cover),
        cover=cover)

app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0'),
    debug=True
)