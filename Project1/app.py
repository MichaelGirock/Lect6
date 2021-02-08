import requests
import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template 
import random

app = Flask(__name__)

AUTH_URL = 'https://accounts.spotify.com/api/token'

random_num =random.randint(1,3)
print(random_num)
if random_num==1:
    BASE_URL = 'https://api.spotify.com/v1/artists/3TVXtAsR1Inumwj472S9r4/top-tracks' #DRAKE
    tracknum =1 #track number
elif random_num==2:
    BASE_URL = 'https://api.spotify.com/v1/artists/04gDigrS5kc9YWfZHwBETP/top-tracks' #MAROON 5
    tracknum =1 #track number
else:
    BASE_URL = 'https://api.spotify.com/v1/artists/6oMuImdp5ZcFhWP0ESe6mG/top-tracks' #MIGOS
    tracknum =1 #track number

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


print(output['tracks'][tracknum]['name'])
print(output['tracks'][tracknum]['artists'][0]['name'])
print(output['tracks'][tracknum]['album']['images'][0]['url'])
print(output['tracks'][tracknum]['preview_url'])

song =(output['tracks'][tracknum]['name'])
artist =(output['tracks'][tracknum]['artists'][0]['name'])
cover = (output['tracks'][tracknum]['album']['images'][0]['url'])
preview=(output['tracks'][tracknum]['preview_url'])

# HTML BELOW [][][][][] HTML BELOW [][][][][] HTML BELOW [][][][][] HTML BELOW [][][][][] HTML BELOW [][][][][] HTML BELOW [][][][][] HTML BELOW [][][][][] HTML BELOW [][][][][] HTML BELOW [][][][][]



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
        cover=cover,
        preview=preview)

app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0'),
    debug=True
)