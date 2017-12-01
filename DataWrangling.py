# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 18:59:17 2017

@author: chris
"""

import pandas as pd
import numpy as np
import math
#used to find the difficulty of the sentences
#import textstat
from textstat.textstat import textstat






#checks to make sure that there are enough sentences to use
def Check_Num_Sentences(df, TotalSentences):
    if len(df) >= TotalSentences:
        return(TotalSentences)
    else:
        return(math.floor(TotalSentences/10)*10)
        
        

def ImportInfo():
    AudioList = pd.read_csv('sentences_with_audio.csv', header = None, sep = '\t')
    Sentences = pd.read_csv('Sentences.csv', header = None, sep = '\t')
    Links = pd.read_csv('links.csv', header = None,sep = '\t')
    
    return([AudioList,Sentences,Links])

def CleanUp(Audio,Sent,Links,Langs):
    #selects only the first column
    #converts the series to a frame, and names the column 'ID'
    
    #selects only the sentences with some sort of license
    #Audio = Audio[(Audio[2] != '\\N') & (Audio[3] != '\\N')]
    
    Audio = Audio.iloc[:,0:3]
    
    #Audio = Audio.to_frame()
    Audio.columns = ['ID','User','License']  
    
    
    
    #renames all of the columns, 
    #selects only the rows that are in one of our src languages    
    Sent.columns = ['ID','Lang','Sentence']
    Sent = Sent[Sent['Lang'].isin(Langs)]
    #print('20')
    
    #names the columns, selects only the rows that in our desired
    #languages, adds tgt, and src languages
    #selects only the sentences with 2 or less translations
    #some sentences have 10 translations that are different 'slang' versions of a 
    #sentence and I don't know how else to deal with this
    Links.columns = ['ID', 'TgtID']
  
    return([Audio,Sent,Links])


def MergeFrames(Audio,Sent,Links):
    AllAudio = pd.merge(Audio,Sent,on = 'ID',suffixes = ('','_y'))
    AllLinks = pd.merge(Links,AllAudio,on = 'ID',suffixes = ('','_y'))
    AllLinks = pd.merge(AllLinks,AllAudio,left_on = 'TgtID', right_on = 'ID'
                        ,suffixes = ('','_y'))
    
    AllLinks.drop('TgtID',axis = 1, inplace = True)
    
    names = ['TgtID','TgtUser','TgtLicense','TgtLang','TgtSent','SrcID','SrcUser','SrcLicense','SrcLang','SrcSent']
    AllLinks.columns = names
    
    return(AllLinks)

def FindDifficulty(df,TgtLang,SrcLang):
    if TgtLang == 'eng':
        col = 'TgtSent'
    elif SrcLang == 'eng':
        col = 'SrcSent'
    else:
        return('Error Message Here')
    
    df['Difficulty'] = ''
    
    df['Difficulty'] = [float(textstat.dale_chall_readability_score(x)) for x in df[col]]  
    
         
    return(df) 
    
#chooses the medium difficulty sentences
def Choose_Difficulty(df,DiffType):
    percentile = np.percentile(df['Difficulty'],np.arange(0,100,25))
    if DiffType == 'Easy':
        MinRange = percentile[0]
        MaxRange = percentile[1]
    
    elif DiffType == 'Medium':
        MinRange = percentile[1]
        MaxRange = percentile[2]
        
    else:
        MinRange = percentile[2]
        MaxRange = percentile[3]
        
    df = df[(df['Difficulty'] >= MinRange) & (df['Difficulty'] <= MaxRange)]
    df.index = np.arange(0,len(df),1)
    return(df)

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

#this function is to get rid of sentences that had more than 1 translation suggestion
def RemoveExtra(df,TgtLang,SrcLang,MaxCount):
    df = df[df.groupby('SrcID').SrcID.transform(len) <= MaxCount]
    df = df[df.groupby('TgtID').TgtID.transform(len) <= MaxCount]
    
    
    df = df[(df['TgtLang'] == TgtLang) & (df['SrcLang'] == SrcLang)]
    return(df)

def check_licences(df):
    df = df[(df['SrcLicense'] != r"\N")  & (df['TgtLicense'] != r"\N")]
    return(df)


def CreateAudioList(TgtLang,SrcLang,MaxCount, difficulty, TotalSentences):
    Audio,Sent,Links = ImportInfo()
    
    Langs = [SrcLang,TgtLang]
    
    Audio,Sent,Links = CleanUp(Audio,Sent,Links,Langs)
    print('we havent merged')
    df = MergeFrames(Audio,Sent,Links)
    print('weve merged')
    df = RemoveExtra(df,TgtLang,SrcLang,MaxCount)
    
    #up until this point the index had no relevence to anything
    #this is starting the index at 0 and + 1 each time
   
    
    if TgtLang.upper() == 'ENG' or SrcLang.upper() == 'ENG':
        df = FindDifficulty(df,TgtLang,SrcLang)
        df = Choose_Difficulty(df,difficulty)
        
    df = check_licences(df)
    
    df = select_few_users(df,TotalSentences)
    
    df.index = np.arange(0,len(df),1)
    
    return(df)
     

  
