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

    def is_already_in(self, path) -> bool:
        return self.encoded_file_name() in os.listdir(path)

    def _details(self) -> str:
        return '"{0}" ===== [{1}] @ {2} (around ~{3} MB)'.format(self.title, self.pafy_object.duration, self.stream.bitrate, self.size())

    def download_to(self, path):
        print("Downloading {0}".format(self._details()))
        download_path = os.path.join(path, self.file_name())
        self.stream.download(filepath=download_path, quiet=True)

        return DownloadedVideo(self)


class DownloadedVideo(Video):

    def then_encode(self):
        pass


video = Video("https://youtu.be/RHFVIH-TewM")
video.download_to("c:\\").then_encode()
