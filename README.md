
# About

spotify-snapshot, because I miss the "recently added to library" features from other music players.

This will create a new playlist in your spotify account, with all music added to your playlists after a certain timestamp added to it. It also tracks all the songs you have, so moving tracks between playlists won't register it as a "new" track. 

## Installation
`pip install -r requirements.txt`
`./install.sh`
Replace the contents of `username.txt` with your spotify username

## Usage
change the `afterThisDate` timestamp variable to the desired time
`python main.py`

