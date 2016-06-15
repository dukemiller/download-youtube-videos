from time import sleep
import subprocess
import threading
import tools
import pafy
import os


class Video:

    _filename = "{}.{}"

    def __init__(self, url, audio=True):
        self.pafy_object = pafy.new(url)
        self.stream = self.pafy_object.getbestaudio() if audio else self.pafy_object.getbestvideo()
        self.desired_extension = "mp3" if audio else "mp4"
        self.title = self.stream.title

    def size(self) -> float:
        return round(self.stream.get_filesize() * 0.000001, 2)

    def file_name(self) -> str:
        return tools.format_filename(self._filename.format(self.title, self.stream.extension))

    def encoded_file_name(self) -> str:
        return tools.format_filename(self._filename.format(self.title, self.desired_extension))

    def is_not_in(self, path) -> bool:
        return self.encoded_file_name() not in os.listdir(path)

    def _details(self) -> str:
        return '"{0}" ===== [{1}] @ {2} (around ~{3} MB)'.format(self.title, self.pafy_object.duration, self.stream.bitrate, self.size())

    def download_to(self, directory) -> 'DownloadedVideo':
        print("Downloading {0}".format(self._details()))

        download_path = os.path.join(directory, self.file_name())
        self.stream.download(filepath=download_path, quiet=True)

        return DownloadedVideo(self, directory, download_path)


class DownloadedVideo:

    def __init__(self, video: Video, directory: str, download_path: str):
        self.video = video
        self.directory = directory
        self.download_path = download_path

    def then_encode(self, in_new_thread=False) -> 'EncodedVideo':
        encoded_path = os.path.join(self.directory, self.video.encoded_file_name())
        command = 'ffmpeg -i "{0}" -f {1} "{2}"'.format(self.download_path, self.video.desired_extension, encoded_path)

        if in_new_thread:
            thread = threading.Thread(target=self._create_process, args=(command,))
            thread.start()
            return EncodedVideo(self.download_path, thread)

        self._create_process(command)
        return EncodedVideo(self.directory)

    @staticmethod
    def _create_process(command: str):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate()


class EncodedVideo:

    def __init__(self, download_path: str, thread: threading.Thread = None):
        self.download_path = download_path
        self.thread = thread

    def and_remove_unencoded_file(self) -> None:
        if self.thread is not None:
            threading.Thread(target=self._sit_and_wait_then_remove).start()
        else:
            os.remove(self.download_path)

    def _sit_and_wait_then_remove(self):
        while self.thread.is_alive():
            sleep(0.2)
        os.remove(self.download_path)
