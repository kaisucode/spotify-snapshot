
import json
from datetime import datetime
import dateutil.parser

import spotipy
import spotipy.util as util

def connect(): 
    aFile = open("username.txt", "r")
    username = aFile.read().split('\n')[0]
    aFile.close()
    #  print(username)

    scope = "user-read-currently-playing user-modify-playback-state user-read-playback-state playlist-modify-public"
    token = util.prompt_for_user_token(username, scope)
    sp = spotipy.Spotify(auth=token)
    return sp, username

def prettyPrint(aJson): 
    print(json.dumps(aJson, indent=4, sort_keys=True))

def retrieveAllItems(results): 
    items = results["items"]
    while results['next']:
        results = sp.next(results)
        items.extend(results['items'])
    return items

def getAllPlaylists(): 
    results = sp.user_playlists(username, limit=50, offset=0)
    playlists = retrieveAllItems(results)
    return playlists

def printPlaylists(playlists): 
    for playlist in playlists:
        print(playlist['id'] + ":\t\t" + playlist["name"])
        #  printTracks(getPlaylistTracks(playlist["id"]))

def getPlaylistTracks(playlistId): 
    results = sp.user_playlist_tracks(username, playlistId)
    tracks = retrieveAllItems(results)
    return tracks

def printTracks(tracks): 
    counter = 0
    for item in tracks: 
        print(item["track"]["name"])
        counter+=1
    print(f"Playlist length: {counter}")

# --------------------------------------------- #

sp, username = connect()

nowString = datetime.now().strftime("%Y-%m-%dT%H%M%SZ")
afterThisDate = dateutil.parser.parse("2020-10-31T00:00:00Z")

lastFile = ""
with open('logs/newestLog.txt', 'r') as outfile:
    timestamp = outfile.read().split('\n')[0]
    lastFile += "logs/" + timestamp + ".json"
    afterThisDate = dateutil.parser.parse(timestamp)

oldSongs = {}
with open(lastFile, 'r') as outfile:
    oldSongs = json.load(outfile)

newTracks = []
currentSongs = {}
#  allPlaylists = {}
allPlaylists = getAllPlaylists()
for playlist in allPlaylists: 
    tracks = getPlaylistTracks(playlist["id"])

    for track in tracks: 

        trackId = track["track"]["id"]
        trackName = track["track"]["name"]
        currentSongs[trackId] = trackName
        #  print(trackId)
        #  print(trackName)

        # check for new songs
        timestamp = dateutil.parser.parse(track["added_at"])
        if (timestamp > afterThisDate) and not(trackId in oldSongs): 
            newTracks.append(trackId)
            print(trackId)
            print(trackName)

newTracks = list(set(newTracks))


# create new playlist
sp.user_playlist_create(username, "spotify-snapshot-" + nowString)
newPlaylistId = ""
newPlaylistName = "spotify-snapshot-" + nowString
newPlaylists = getAllPlaylists()
for playlist in newPlaylists: 
    if (playlist["name"] == newPlaylistName): 
        newPlaylistId = playlist["id"]

numOfAdds = len(newTracks)//100 + 1
for i in range(0, numOfAdds): 
    fromNum = i * 100
    toNum = (i + 1) * 100
    partialTracks = newTracks[fromNum:toNum]
    sp.user_playlist_add_tracks(username, newPlaylistId, partialTracks)

newFilename = 'logs/' + nowString + ".json"
with open(newFilename, 'w') as outfile:
    json.dump(currentSongs, outfile)

with open('logs/newestLog.txt', 'w') as outfile:
    outfile.write(nowString)




#----------------


#  playlists = sp.user_playlists('spotify')
#  prettyPrint(playlists)

