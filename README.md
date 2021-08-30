# realtime-slideshow
Realtime photo slideshow with [Swiper.js](http://idangero.us/swiper/) and [DropboxFileRequest](https://help.dropbox.com/files-folders/share/create-file-request).

<img src=https://github.com/WSShiro/realtime-slideshow/blob/master/example/diagram1.png width=70%>
  
- [Example](#example)
- [Usage](#usage)
- [Prior Art](#prior-art)
- [License](#license)


## Example
<img src=https://github.com/WSShiro/realtime-slideshow/blob/master/example/example2.gif width=70%>
Here Mr. John Smith posted 2 photos and, a few seconds later, he posted 3 photos additionally.  


## Usage
Edit the directory path, where images come in, at `path=` in [start.py](/start.py).
```
path = os.getcwd()+'\DropboxPhoto'
```
Run start.py to keep updating a image list json file.
```
py start.py
```
Open [index.html](/index.html).  

Press space bar to show "Please wait momentarily" image.  
Press Q key to show "Slideshow has ended" image.

You may need to change some browser option to access local files.
For Chrome, boot option " --args --allow-file-access-from-files" may be needed.


## Prior Art
Many thanks to [knight_photo_contest](https://github.com/ktkiyoshi/knight_photo_contest) giving me my starting point.
Also thanks to [Python Exif Modification](https://kapibara-sos.net/archives/658) and [tree-json](https://github.com/acro5piano/tree-json).


## License
This software is released under the [MIT lincese](https://github.com/WSShiro/realtime-slideshow/blob/master/LICENSE).