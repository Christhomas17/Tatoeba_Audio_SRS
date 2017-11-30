
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


from DataWrangling import CreateAudioList
from SRS import GetSRS
from AudioWrangling import DownloadAll, Create_Files


##########################################
####USER DEFINED VARIABLES

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


###########################################

def check_first_time():

    if firstTime == 'Yes':        
        subprocess.call('FirstTime.py', shell = True)
        print('All files downloaded')

def select_few_users(df,TotalSentences):
    tgtCounts = df['TgtUser'].value_counts()
    srcCounts = df['SrcUser'].value_counts()
    
    #let's remove the counts that are less than 20
    for index,count in enumerate(tgtCounts):
        if count <= 20:
            tgtCounts = tgtCounts[0:index]
            
    for index,count in enumerate(srcCounts):
        if count <= 20:
            srcCounts = srcCounts[0:index]
            
    
    
    
    #let's figure out how many users we need to go through
    maxUserCount = max(srcCounts.count(), tgtCounts.count())
    
    y = pd.DataFrame()
    tgtUsers = []
    srcUsers = []
    
    for index in range(maxUserCount):
        try:
            tgtUsers.append(tgtCounts.index[index])
            srcUsers.append(srcCounts.index[index])
        except:
            pass
        
        y = df[(df['TgtUser'].isin(tgtUsers)) & (df['SrcUser'].isin(srcUsers))]
    if len(y) >= TotalSentences:
        return(y)
    else:
        return(df)
        
  
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
    df = CreateAudioList(TgtLang,SrcLang,MaxCount)
    df = select_few_users(df,TotalSentences)
    
    srs,Indices,Groups = GetSRS(df,TotalSentences,SentsPerDay,Interval,Times)
    
    Folder = create_media_folder()
    DownloadAll(df,Indices,TgtLang,SrcLang,Folder,BaseURL)
    Create_Files(df, Indices, srs, Groups, Folder, RepeatTimes)
    
    SelectedMedia = df.loc[Indices,:]
    SelectedMedia.to_csv('SelectedMedia.csv',sep = ',')
    
    
    return(df)
    
if __name__ == '__main__':
    df = main()
    
