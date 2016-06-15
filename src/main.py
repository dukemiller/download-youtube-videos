from youtube import Video


def main():
    video = Video("https://youtu.be/RHFVIH-TewM")
    path = r"c:\users\duke\downloads"

    if video.is_not_in(path):
        video.download_to(path)\
            .then_encode(in_new_thread=True)\
            .and_remove_unencoded_file()

if __name__ == '__main__':
    main()
