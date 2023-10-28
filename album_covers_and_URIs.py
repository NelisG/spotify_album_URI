import argparse
import logging
import os
from pathlib import Path

import pandas as pd
import requests
import spotipy
import spotipy.util as util

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

SPOTIFY_CLIENT_ID = '<FILL_IN>'
SPOTIFY_CLIENT_SECRET = '<FILL_IN>'

SCOPE = 'user-top-read'
SPOTIFY_REDIRECT_URI = 'http://example.com/callback/'
COVER_DIRECTORY = Path("Covers")
NUMBER_OF_ARTISTS = 5
ALBUMS_PER_ARTIST = 10  # max 20


class AlbumUriFetcher:

    def __init__(self, spotify_username: str) -> None:
        self.spotify_username = spotify_username
        token = util.prompt_for_user_token(spotify_username, SCOPE, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI)
        self.sp = spotipy.Spotify(auth=token)

    def get_top_artists(self) -> list:
        """Get a user's top artists from Spotify."""
        limit_per_page = 5
        top_artists = []
        for i in range(0, NUMBER_OF_ARTISTS, limit_per_page):
            artist_dict = self.sp.current_user_top_artists(limit=limit_per_page, offset=i, time_range='medium_term')
            top_artists = top_artists + artist_dict["items"]
        return top_artists

    def process_album(
            self,
            album: dict,
            artist_name: str,
            artist_album_folder: Path
    ) -> None:
        """Process an album by adding its information to the relevant output lists and storing its cover to a file."""

        album_name = get_cleaned_string(album["name"])
        album_uri = album["uri"]
        description = f"{artist_name}: {album_name}".encode('utf-8')

        # Add album data to relevant lists
        self.basic_album_info_output.append([artist_name, album_name, album_uri])
        self.tagwriter_output.append(f"Text,{album_uri},,{description},,,\n")

        # Write album cover to file
        img_data = requests.get(album['images'][0]['url']).content
        with open(f"{artist_album_folder}/{album_name}.jpg", 'wb') as handler:
            handler.write(img_data)

        logger.info("Processed album %s - %s", artist_name, album_name)

    def run(self) -> None:
        self.tagwriter_output = ["Type (Link/Text),Content (http://....),URI type (URI/URL/File...),Description,Interaction counter,UID mirror,Interaction counter mirror\n"]
        self.basic_album_info_output = []

        top_artists = self.get_top_artists()
        for i, artist in enumerate(top_artists):
            artist_name = get_cleaned_string(artist["name"])

            artist_album_folder = COVER_DIRECTORY / f"{i}-{artist_name}"
            if not os.path.isdir(artist_album_folder):
                os.makedirs(artist_album_folder)

            albums = self.sp.artist_albums(artist["id"], limit=ALBUMS_PER_ARTIST)['items']
            for album in albums:
                self.process_album(album, artist_name, artist_album_folder)

        # Write respective outputs to file
        with open("Tagwriter_mass_encoding.csv", 'w') as f:
            for tagwriter_output_line in self.tagwriter_output:
                f.write(tagwriter_output_line)

        df = pd.DataFrame(self.basic_album_info_output, columns=['Artist', 'Album', 'Album_URI '])
        df.to_csv("artist_album_URI.csv", index=False, encoding='utf-8')

        logger.info('---Found %s album covers for %s artists---', len(self.basic_album_info_output), len(top_artists))


def get_cleaned_string(s: str) -> str:
    """Remove non-alphanumeric characters from a string."""
    return ''.join(e for e in s if e.isalnum() or e == " ")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get album covers and URIs from Spotify')

    parser.add_argument('spotify_username', type=str, help='Spotify username')
    args = parser.parse_args()

    fetcher = AlbumUriFetcher(args.spotify_username)
    fetcher.run()
