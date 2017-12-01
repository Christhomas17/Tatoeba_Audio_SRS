
'''

1) Check if first time using pop-up
    1a) download the excel files
    2a) download and handle ffmpeg
    3a) install the necessary packages
2) Determine user languages
3) determine how many sentence pairs are available
4) decide if voice-to-text should be used
5) create srs algorith depending on the number of sentences and days
6) combine the sentences and sort according to srs


'''

'''
Please navigate to this page
http://ffmpeg.zeranoe.com/builds/
Download the correct build for your system. Then unzip this file, and copy the 
"bin" folder directly into the same folder as where you have all of the other 
Python scripts

'''


import subprocess
import os
import pandas as pd
import pydub
import datetime


from DataWrangling import CreateAudioList
from SRS import GetSRS
from AudioWrangling import DownloadAll, Create_Files


##########################################
####USER DEFINED VARIABLES

SrcLang = 'eng'
TgtLang = 'spa'

TotalSentences = 200
SentsPerDay = 10

RepeatTimes = 2

MaxCount = 1

Interval = [0,1,1,2,4,8,16,26,38,50,64,78,80]

Times = [8,6,4,3,2,1]

difficulty = 'Hard'

BaseURL = 'https://audio.tatoeba.org/sentences/'

firstTime = 'No'

cwd = os.getcwd()
pydub.AudioSegment.converter = os.path.join(cwd,r"bin\ffmpeg.exe")


###########################################

def check_first_time():

    if firstTime == 'Yes':        
        subprocess.call('FirstTime.py', shell = True)
        print('All files downloaded')


        
  
def create_media_folder():
    Folder = os.path.join(os.getcwd(),'Media')
    
    #checks if the folder exists. If it doesn't, creates it
    try:
        os.stat('Media')
    except:
        os.mkdir(Folder)
        
    return(Folder)    
    
def main():
    check_first_time()
    df = CreateAudioList(TgtLang,SrcLang,MaxCount, difficulty,TotalSentences)  
    
    srs,Indices,Groups = GetSRS(df,TotalSentences,SentsPerDay,Interval,Times)
    
    Folder = create_media_folder()
    DownloadAll(df,Indices,TgtLang,SrcLang,Folder,BaseURL)
    Create_Files(df, Indices, srs, Groups, Folder, RepeatTimes)
    
    SelectedMedia = df.loc[Indices,:]
    title = TgtLang + '-' + SrcLang + '-' + str(datetime.datetime.today().date()) + '.xlsx'    
    title = os.path.join(cwd,title)
    SelectedMedia.to_csv(title,sep = ',')
    
    
    return(df)
    
#if __name__ == '__main__':
#    df = main()
    
