# download-youtube-videos
A simple script to download youtube videos and playlists (and optionally encode them to mp3) using pafy and FFMPEG. It's focused around downloading audio streams only, but it's possible to download videos by changing something somewhere in the files.   
  
*Requires:* [FFMPEG](https://ffmpeg.org/download.html) on PATH  
  
### Calling
**command line --**  
``python {main.py} {youtube url} {directory}``  
``{main.py}`` => the file path to main.py   
``{youtube url}`` => the youtube url (either a playlist or single video link)   
``{directory}`` => the path that file should be downloaded to  
  
e.g. ``python main.py https://youtu.be/d0Gd4EjbKk4 .``  
Download the video to current directory.    

**OR**  

**interactive --**
``python {main.py}``  
``{main.py}`` => the file path to main.py   
Prompts will come up for the same arguments as the commandline to be filled out in exactly the same way.  


