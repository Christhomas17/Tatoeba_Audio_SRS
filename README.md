# Tatoeba_Audio_SRS
These scripts will create spaced-repitition audio files in order to help learn/practice a second language
The audio being used is available under a public license.

You can find sample files [here](https://soundcloud.com/chris-thomas-425694789/sets/tatoeba-audio-srs). These files assume English as the native language and Spanish as the target language(That's me) 

# Tatoeba Audio Spaced Repitition System

This script will use a very simple spaced repititon system( you can find out about spaced repititon [here](https://en.wikipedia.org/wiki/Spaced_repetition)) to create audio files of sentences in 2 languages, a student's native language and the target language that they are trying to learn. All of the audio files and sentences are user curated and are freely available on Tatoeba.org. 

### Python Installation
 - If you have no idea what Python is and you don't have it installed, I recommend [this](https://www.anaconda.com/download/) piece of software. Its called Anaconda. It removes some of the headache of installing Python. It's a large file and you want, you can always just download Python from [here](https://www.python.org/downloads/) 
 - Make sure you download python 3.x, not 2.x. These are very different things. 

### Once you have Python 3.x installed
- You need to download ffmpeg on your own. This software allows Python to interact directly with the audio files. Go [here](http://ffmpeg.zeranoe.com/builds/), download the proper version for your operating system. 
  - Unzip the archive
  - Copy the "bin" folder directly into the same folder where you have all of the Python scripts
- The rest should be taken care of Python so let's just change some variable so Python knows what to do. Open up the 'New.py' file and you should see the following variables:
```Python
SrcLang = 'eng'
TgtLang = 'spa'

TotalSentences = 20
SentsPerDay = 10

RepeatTimes = 2

MaxCount = 1

Interval = [0,1,1,2,4,8,16,26,38,50,64,78,80]

Times = [8,6,4,3,2,1]

BaseURL = 'https://audio.tatoeba.org/sentences/'

firstTime = 'No'

cwd = os.getcwd()
pydub.AudioSegment.converter = os.path.join(cwd,r"bin\ffmpeg.exe")
```
