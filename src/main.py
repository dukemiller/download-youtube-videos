from collections import namedtuple
from typing import Iterable
from video import Video
import sys
import pafy
import os

UrlResult = namedtuple('Result', 'successful url type')
DirectoryResult = namedtuple('Result', 'successful path')


def get_directory(path: str = None) -> DirectoryResult:

    if path is None:
        path = input("Download path: ")

    if path == "":
        question = input("Default to users download folder? [y/n]: ")
        while not question == "y" and not question == "n":
            question = input("Default to users download folder? [y/n]: ")
        if question == "n":
            return DirectoryResult(successful=False, path=path)
        path = os.path.join(os.path.expanduser("~"), "Downloads")

    if not os.path.exists(path):
        question = input("Path does not exist. Create? [y/n]: ")
        while not question == "y" and not question == "n":
            question = input("Path does not exist. Create? [y/n]: ")
        if question == "n":
            return DirectoryResult(successful=False, path=path)
        os.makedirs(path)

    return DirectoryResult(successful=True, path=path)


def get_url_information(urls: Iterable[str] = None) -> Iterable[UrlResult]:

    if urls is None:
        urls = input("Enter url/s: ").split(" ")

    collection = []

    for url in urls:
        
        url = url.lstrip(" ").strip().replace("\s+", "\s")

        if 'youtube' not in url and 'youtu.be' not in url:
            collection.append(UrlResult(successful=False, url=url, type=''))

        # id exists
        if "?v=" in url:
            url = url.split("&")[0]
            collection.append(UrlResult(successful=True, url=url, type='single_video'))

        elif '&list=' in url:
            playlist_id = url.split("&list=")[1].split("=")[0]
            url = "https://www.youtube.com/playlist?list={0}".format(playlist_id)
            collection.append(UrlResult(successful=True, url=url, type='playlist'))

        elif '/playlist?list' in url:
            playlist_id = url.split("/playlist?list=")[1].split("=")[0]
            url = "https://www.youtube.com/playlist?list={0}".format(playlist_id)
            collection.append(UrlResult(successful=True, url=url, type='playlist'))

        else:
            collection.append(UrlResult(successful=True, url=url, type='single_video'))

    return collection


def get_videos_from(result: UrlResult) -> Iterable[Video]:
    if result.type == "single_video":
        yield Video(result.url)

    elif result.type == "playlist":
        try:
            for video in pafy.get_playlist(result.url)['items']:
                try:
                    yield Video(video['pafy'])
                except:
                    continue

        except ValueError:
            print("Playlist is missing/private.")


def main():
    if len(args) > 1:
        if len(args) == 2:
            exit("Incorrect number of arguments.")
        path, urls = args[1], args[2:]

    else:
        path, urls = None, None

    directory = get_directory(path)

    if not directory.successful:
        exit("Unable to proceed.")

    for result in get_url_information(urls):

        if not result.successful:
            print("Malformed url {0}.".format(result.url))
            continue

        for video in get_videos_from(result):
            if video.is_not_in(directory.path):
                video.download_to(directory.path) \
                     .then_encode(in_new_thread=True) \
                     .and_remove_unencoded_file()

if __name__ == '__main__':
    args = sys.argv
    main()
