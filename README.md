# spotify_album_URI

## Overview
This repo contains the Python code to download the album covers and album information of your most played artists on Spotify. This code is used in an Instructable [Albums-With-NFC-Tags-to-Automatically-Play-Spotify](https://www.instructables.com/id/Albums-With-NFC-Tags-to-Automatically-Play-Spotify/) where I show how to use NFC tags to automatically play an album on Spotify by tapping the album cover with your phone.

## Prerequisites

### Python Environment
You need a Python environment with the following packages installed:
* `spotipy`
* `pandas`

You can install these packages using the requirements.txt file by:
```
pip install -r requirements.txt
```

### Spotify API credentials

You will need to provide your Spotify API credentials in the `album_covers_and_URIs.py` file. Here's how you can obtain these credentials:

1. Create a Spotify developer account at [Spotify Developer](https://developer.spotify.com).
2. After creating an account, create a new application.
3. Copy the Client ID and Client Secret from your newly created application.
4. Paste these into the corresponding constants (`SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`) in the `album_covers_and_URIs.py` file.


## Usage

```
python album_covers_and_URIs.py <Spotify_username>
```

The first time you run the script, a link will open in your default browser. This is to give the application access to modify your Spotify playlists with the scope `user-top-read`. After giving the application access, you are directed to a link starting with http://example.com/... Copy the whole link and paste it in the terminal or command prompt to give the script the necessary permissions. 

The output of the script consists of:
* a folder `Covers` containing the album covers of your most played artists
* a file `album_covers_and_URIs.csv` containing the album information and URIs of the albums
* a file `Tagwriter_mass_encodings.csv` containing the mass_encodings data needed to write the NFC tags.

For more information on how to use these files, have a look at the Instructable [Albums-With-NFC-Tags-to-Automatically-Play-Spotify](https://www.instructables.com/id/Albums-With-NFC-Tags-to-Automatically-Play-Spotify/).

