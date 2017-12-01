# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 20:13:21 2017

@author: chris
"""

#used for audio file manipulation
import pydub
from pydub import AudioSegment 

#used to download the files
import urllib.request

import os


######################################################
#Downloads the files and merges them into the audio files that we need
def DLFile(ID,Lang,Folder,BaseURL):
    URL = BaseURL + Lang + '/' + ID  + '.mp3'
    

    #I thought that this was already taken care of in the main file??
    if not os.path.exists(Folder):
        os.makedirs(Folder)
        
    
    #FileName = Lang +'-' + ID + '.mp3' 
    FileName = ID + '.mp3'
    FileName = os.path.join(Folder,FileName)


    #downloads the file
    if os.path.exists(FileName):
        print("We didn't download a file")
        pass
    else:
        urllib.request.urlretrieve(URL,FileName)
    
def DownloadAll(df, Indices,TgtLang ,SrcLang,Folder,BaseURL):
    NumFiles = len(Indices)    


    for i in range(NumFiles):
        SrcID = str(df.loc[Indices[i],'SrcID'])
        TgtID = str(df.loc[Indices[i],'TgtID'])
        
        DLFile(TgtID,TgtLang,Folder,BaseURL)
        DLFile(SrcID,SrcLang,Folder,BaseURL)
        print('You have downloaded ' + str((i+1)*2) + ' files.')
        
def CreateOneSentence(TgtID,SrcID,Index,Folder):
    
    
    
    tgt = AudioSegment.from_mp3(os.path.join(Folder,TgtID + '.mp3'))
    
    TgtDur = tgt.duration_seconds
    Silence = AudioSegment.silent(duration = TgtDur*1000)
    #Silence = AudioSegment.silent(duration = 5000)
    src = AudioSegment.from_mp3(os.path.join(Folder,SrcID + '.mp3'))
    #src = AudioSegment.from_mp3(os.path.join(Folder,SrcID + '.mp3'))
    
    file = tgt + Silence + src
    
    os.chdir(Folder)
    file.export(Index + '.mp3',format = 'mp3')  
    
def Create_First_Day_Sentence(TgtID,SrcID,Index,Folder,RepeatTimes):   
    tgt = AudioSegment.from_mp3(os.path.join(Folder,TgtID + '.mp3'))
    
    TgtDur = tgt.duration_seconds
    Silence = AudioSegment.silent(duration = TgtDur*1000)
    #Silence = AudioSegment.silent(duration = 5000)
    src = AudioSegment.from_mp3(os.path.join(Folder,SrcID + '.mp3'))
    #src = AudioSegment.from_mp3(os.path.join(Folder,SrcID + '.mp3'))
    
    file = tgt
    for i in range(RepeatTimes - 1):
        file += Silence + tgt
        
    file += Silence + src
        
        
    #file = tgt + Silence + tgt + Silence + src
    os.chdir(Folder)
    file.export(Index +  '-1' + '.mp3',format = 'mp3')  
    

    
    
def CombineAllSentences(df,Indices, Folder):
    
    
    for Index in Indices:

        TgtID = str(df['TgtID'][Index])
        SrcID = str(df['SrcID'][Index])
        
        Index = str(Index)
        
        CreateOneSentence(TgtID,SrcID,Index,Folder)
        #Create_First_Day_Sentence(TgtID,SrcID,Index,Folder,Times = 2)
    
    
def CreateDailyAudioFiles(df,Indices,srs):
    Silence = AudioSegment.silent(duration = 1000)    

    for day in range(len(srs)):
        song = AudioSegment.empty()
        for item in srs[day]:
            song += AudioSegment.from_mp3(str(item) + '.mp3')
          
        #adds a short silence between each new phrase    
        song += Silence
            
        song.export('Day' + str(day+1) + '.mp3',format = 'mp3')
       
        
def Create_Files(df, Indices, srs, Groups, Folder, RepeatTimes):
    
    
    for Index in Indices:

        TgtID = str(df['TgtID'][Index])
        SrcID = str(df['SrcID'][Index])
        
        Index = str(Index)
        
        CreateOneSentence(TgtID,SrcID,Index,Folder)
        Create_First_Day_Sentence(TgtID,SrcID,Index,Folder,RepeatTimes)
        
     
    Silence = AudioSegment.silent(duration = 1000)  
    
    for day in range(len(srs)):
        song = AudioSegment.empty()
        
        for item in srs[day]:
            #checks to see if this is the first time you are
            #hearing a song
            if day < len(Groups):
                if item in Groups[day]:
                    filename = str(item) + '-1' + '.mp3'
                else:
                    filename = str(item) + '.mp3'
                    
            else:
                filename = str(item) + '.mp3'
            
            song += AudioSegment.from_mp3(filename)


        #adds a short silence between each new phrase    
        song += Silence
            
        song.export('Day' + str(day+1) + '.mp3',format = 'mp3')
        

        
