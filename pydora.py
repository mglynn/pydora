import argparse
import sys
import urllib.request
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup

def get_similar_artists(artist):
    """Returns a list of similar artists."""
    artist = artist.replace(' ', '-').lower()
    url = 'http://pandora.com/xml/music/artist/'

    tree = ET.parse(urllib.request.urlopen(url + artist))
    root = tree.getroot()

    similar_artists = [artist.get('name') for artist in root.iter('artist')]

    return similar_artists

def get_similar_songs(artist, song):
    """Returns a list of similar songs with their respective artists."""
    artist = artist.replace(' ', '-').lower()
    song = song.replace(' ', '-').lower()
    url = 'http://www.pandora.com/music/song/'

    page = urllib.request.urlopen(url + artist + '/' + song)
    soup = BeautifulSoup(page.read())

    similar_songs_title = soup.findAll('div', {'class': 'similar_title'})
    similar_songs_artist = soup.findAll('div', {'class': 'similar_artist'})

    titles = [title['title'] for title in similar_songs_title]
    artists = [artist['title'] for artist in similar_songs_artist]

    return list(zip(titles, artists))

def main():
    parser = argparse.ArgumentParser(description='Query Pandora for information about artists and their songs.')
    parser.add_argument('-a', '--artist', dest='artist', help='Input artist name', required=True)
    parser.add_argument('-s', '--song', dest='song', help='Input song name')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()
    if args.song:
        print(get_similar_songs(args.artist, args.song))
    else:
        print(get_similar_artists(args.artist))

if __name__ == '__main__':
    sys.exit(main())