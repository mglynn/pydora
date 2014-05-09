import argparse
import sys
import urllib.request
import xml.etree.ElementTree as ET


def get_similar_artists(artist):
    """Returns a list of similar artists."""
    artist = artist.replace(' ', '-').lower()

    url = 'http://pandora.com/xml/music/artist/'
    url = ''.join("{}{}".format(url, artist))

    tree = ET.parse(urllib.request.urlopen(url))
    root = tree.getroot()

    artists = [artist.get('name') for artist in root.iter('artist')]

    return artists


def get_similar_songs(artist, song):
    """Returns a list of similar songs with their respective artists."""
    artist = artist.replace(' ', '-').lower()
    song = song.replace(' ', '-').lower()

    url = 'http://www.pandora.com/xml/music/song/'
    url = ''.join("{}{}{}{}".format(url, artist, '/', song))

    tree = ET.parse(urllib.request.urlopen(url))
    root = tree.getroot()

    artists = [artist.get('artistName') for artist in root.iter('song')]
    titles = [song.get('songTitle') for song in root.iter('song')]

    return list(zip(titles, artists))


def main():
    parser = argparse.ArgumentParser(description='Query Pandora for \
        information about artists and their songs.')
    parser.add_argument('-a', '--artist', dest='artist', help='Input artist \
        name', required=True)
    parser.add_argument('-s', '--song', dest='song', help='Input song name')

    args = parser.parse_args()
    if args.song:
        print(get_similar_songs(args.artist, args.song))
    else:
        print(get_similar_artists(args.artist))

    return 0


if __name__ == '__main__':
    sys.exit(main())
