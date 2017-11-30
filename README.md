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

firstTime = 'No'

pydub.AudioSegment.converter = os.path.join(cwd,r"bin\ffmpeg.exe")
```
  - The SrcLang is your native language while the target language is the language you are trying to learn. The 3 letter codes that you should use can be found on Tatoeba [here](https://tatoeba.org/eng/stats/sentences_by_language). Obviously, the more sentences available for your language, the better.
  - TotalSentences represents the total number of sentences that you want to learn. I recommend keeping this at 20 the first time you run this script just to make sure it works but then you can change it to what you like
  - SentsPerDay represents the number of new sentences per day, not total sentences. 10 seems to be a good number but do what you will
  - Repeat times represents how many times you wany to repeat the new sentence in your target language before hearing the native language version. This only happens on the first day. On the following days, you will hear the target language followed by a short pause and then the native version
  - MaxCount is set to 1. This gets rid of sentences that have more than 1 translation. If your language doesn't have enough samples, feel free to change this to a higher number
  - Interval represents my version of a spaced repitition system. Those numbers represent the days when you are going to hear the sentence. So for example, let's say you are hearing the sentence, 'Hello World' for the first time on day 3. You will hear this sentence on day 3, day 4,5,7,11 etc.
  - Times. This represents how many times the sentence will be repeated. In my example, the first day that you hear a sentence, it will be repeated 8 times, the second day 6 times. Any day the sentence is heard after those initial 6 days, it will only be heard once.
  - pydub.AudioSegment.converter - This represents where the ffmpeg folder is located. If you followed my directions above, you don't need to change this. 
