import requests
import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template 
import random
from bs4 import BeautifulSoup
import re


load_dotenv(find_dotenv())


app = Flask(__name__)

AUTH_URL = 'https://accounts.spotify.com/api/token'

random_num =random.randint(1,3)
#print(random_num)
if random_num==1:
    BASE_URL = 'https://api.spotify.com/v1/artists/2oX42qP5ineK3hrhBECLmj/top-tracks' #Andy Grammer
    tracknum =4 #track number
elif random_num==2:
    BASE_URL = 'https://api.spotify.com/v1/artists/7gXb99Sf9nNmpNYeAgIQFG/top-tracks' #Sub Urban Craddles
    tracknum =0 #track number
else:
    BASE_URL = 'https://api.spotify.com/v1/artists/2tIP7SsRs7vjIcLrU85W8J/top-tracks' #The Kid LAROI WITHOUT YOU
    tracknum =0 #track number


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


#print(output['tracks'][tracknum]['name'])
#print(output['tracks'][tracknum]['artists'][0]['name'])
#print(output['tracks'][tracknum]['album']['images'][0]['url'])
#print(output['tracks'][tracknum]['preview_url'])

song =(output['tracks'][tracknum]['name'])
artist =(output['tracks'][tracknum]['artists'][0]['name'])
cover = (output['tracks'][tracknum]['album']['images'][0]['url'])
preview=(output['tracks'][tracknum]['preview_url'])

#-------------------------------------------------------------------------------------------------------------GENIUS
gclient_access_token = os.getenv('GENIUS_ACCESS_TOKEN')
gbase_url = 'https://api.genius.com'
#song = "wap by carti b"
guser_input = song

path = 'search/'
grequest_uri = '/'.join([gbase_url, path])

gparams = {'q': guser_input}

gauth_token = 'Bearer {}'.format(gclient_access_token)

#genius_id = os.getenv('GENIUS_ID')
#genius_secret = os.getenv('GENIUS_SECRET')
#auth_token = b64encode(str.encode(f"{genius_id}:{genius_secret}")).decode("ascii")
gheaders = {
    'Authorization': gauth_token
}

grequest = requests.get(grequest_uri, params=gparams, headers=gheaders)

#this gives the link for the lyrics page of the searched song.
#This is for the first result of the search. You can use a for loop if you want the URL for more results.
r=grequest.json()

URL = r['response']['hits'][0]['result']['url']

#to get the lyrics out of the page I used beautifulsoup in the following way.
page = requests.get(URL)
print (URL)
#-------------------------------------------------------------------------------------------------------------GENIUS

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
        preview=preview,
        geniuslink=URL)

app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0'),
    debug=True
)