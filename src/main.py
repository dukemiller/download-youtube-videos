from collections import namedtuple
from typing import Iterable
from youtube import Video
import pafy
import os

UrlResult = namedtuple('Result', 'successful url type')
PathResult = namedtuple('Result', 'successful path')


def get_path() -> PathResult:

    path = input("Download path: ")

    if path == "":
        question = input("Default to users download folder? [y/n]: ")
        while not question == "y" and not question == "n":
            question = input("Default to users download folder? [y/n]: ")
        if question == "n":
            return PathResult(successful=False, path=path)
        path = os.path.join(os.path.expanduser("~"), "Downloads")

    if not os.path.exists(path):
        question = input("Path does not exist. Create? [y/n]: ")
        while not question == "y" and not question == "n":
            question = input("Path does not exist. Create? [y/n]: ")
        if question == "n":
            return PathResult(successful=False, path=path)
        os.makedirs(path)

    return PathResult(successful=True, path=path)


def get_url_information() -> UrlResult:

    url = input("Enter url: ").strip()

    if 'youtube' not in url and 'youtu.be' not in url:
        return UrlResult(successful=False, url=url, type='')

    if '&list=' in url:
        playlist_id = url.split("&list=")[1].split("=")[0]
        url = "https://www.youtube.com/playlist?list={0}".format(playlist_id)
        return UrlResult(successful=True, url=url, type='playlist')

    if '/playlist?list' in url:
        playlist_id = url.split("/playlist?list=")[1].split("=")[0]
        url = "https://www.youtube.com/playlist?list={0}".format(playlist_id)
        return UrlResult(successful=True, url=url, type='playlist')

    return UrlResult(successful=True, url=url, type='single_video')


def get_videos_from(result: UrlResult) -> Iterable[Video]:

    if result.type == "single_video":
        yield Video(result.url)

    elif result.type == "playlist":
        for video in pafy.get_playlist(result.url)['items']:
            yield Video(video['pafy'])

    else:
        yield []


def main():

    url_information = get_url_information()
    if not url_information.successful:
        exit("Malformed url.")

    path = get_path()
    if not path.successful:
        exit("Unable to proceed.")

    for video in get_videos_from(url_information):
        if video.is_not_in(path.path):
            video.download_to(path.path) \
                 .then_encode(in_new_thread=True) \
                 .and_remove_unencoded_file()

if __name__ == '__main__':
    main()
