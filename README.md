# Python Music Player 

  A simple python music player created using tkinter GUI library..
  
<br> 
<br>
  
  
## Changelog: 
  - added a tilde (~) Button that can add a single song to the current collection / playlist
  - added logic to avoid multiple instances of the same song to be in the same collection
  
  <br>
  
  ## Dependencies
  
   ### Mutagen
    
   Mutagen is a Python module to handle audio metadata. It supports ASF, FLAC, MP4, Monkey’s Audio, MP3, Musepack, Ogg Opus, Ogg FLAC, Ogg Speex, Ogg Theora, Ogg Vorbis, True Audio, WavPack, OptimFROG, and AIFF audio files. All versions of ID3v2 are supported, and all standard ID3v2.4 frames are parsed. It can read Xing headers to accurately calculate the bitrate and length of MP3s. ID3 and APEv2 tags can be edited regardless of audio format. It can also manipulate Ogg streams on an individual packet/page level.

Mutagen works with Python 3.6+ (CPython and PyPy) on Linux, Windows and macOS, and has no dependencies outside the Python standard library. Mutagen is licensed under the GPL version 2 or later.

For more information visit https://mutagen.readthedocs.org
https://codecov.io/gh/quodlibet/mutagen/branch/master/graph/badge.svg

<br>

  ### Pygame
  
  Pygame is a set of Python modules designed for writing video games. Pygame adds functionality on top of the excellent SDL library. This allows you to create fully featured games and multimedia programs in the python language.

Pygame is highly portable and runs on nearly every platform and operating system.

<br>

  ### Pillow 
  
  Pillow is built on top of PIL (Python Image Library). PIL is one of the important modules for image processing in Python. However, the PIL module is not supported since 2011 and doesn’t support python 3.

Pillow module gives more functionalities, runs on all major operating system and support for python 3. It supports wide variety of images such as “jpeg”, “png”, “bmp”, “gif”, “ppm”, “tiff”. You can do almost anything on digital images using pillow module. Apart from basic image processing functionality, including point operations, filtering images using built-in convolution kernels, and color space conversions.

<br>
<br>

## Installing all the dependencies

  ```python
      python3 -m pip install Mutagen
      python3 -m pip install Pygame
      python3 -m pip install Pillow
  ```
