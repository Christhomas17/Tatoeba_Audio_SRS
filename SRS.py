# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 19:58:02 2017

@author: chris
"""
import pandas as pd
import numpy as np
import random as rd

################################
#Does the SRS(Spaced Repition) Dirty Work

def ChooseIDs(df,TotalSentences,SentsPerDay):
    
    length = len(df)
    
    if TotalSentences <= length:
        NumPicks = TotalSentences
    else:
        NumPicks = length
    
    
    #gets a random sample of all of the IDs that we have available to use
    IDs = rd.sample(set(np.arange(0,length,1)),NumPicks)
    
    #groups the IDs into what i refer to as "days"
    Groups = [IDs[(SentsPerDay*x):(SentsPerDay*x + SentsPerDay)] for x in range(int(TotalSentences/SentsPerDay))]
    
    
    
    
    return([Groups,IDs]) 

def CreateSRSFrame(df,groups,Interval,Times):
    
    
    
    #rows
    NumGroups = len(groups)
    #columns
    NumDays = len(groups[0])
    NumCols = NumGroups + NumDays + sum(Interval)+ 3
    
    #makes it so that Times is the same length as Interval
    Times.extend([1]*(len(Interval) - len(Times)))
    
    #adding the 3 just because. it shouldn't be needed
    y = pd.DataFrame(np.zeros((NumGroups,NumCols),dtype = object))
    
    for group in range(NumGroups):
        
        for day in range(NumDays):
            
            try:
                #SRS.iloc[group,day + Interval[day]+ group] = Times[day] #groups[day]*Times[day]
                y.iloc[group,day + Interval[day]+ group] = Times[day]*groups[group]
            except:
                print('stuff')      
                
    x = [   [] for z in range(NumCols)]
            
    for day in range(len(y.columns)):
        
       
        for group in range(len(y.index)):
           
            if y.iloc[group,day] != 0:
                x[day] += y.iloc[group,day]
                        
                
    #shuffles each day so that the order is different each day
    [rd.shuffle(x[h]) for h in range(len(x))]
    
    
    return(x)    

def Remove_Empty_Srs(srs):
    temp = [srs[day]  for day in range(len(srs)) if len(srs[day]) > 0 ]
    srs = temp
    
    return(srs)
    


def GetSRS(df,TotalSentences,SentsPerDay,Interval, Times):
    Groups, IDs = ChooseIDs(df, TotalSentences,SentsPerDay)
    SRS = CreateSRSFrame(df,Groups,Interval, Times)
    SRS = Remove_Empty_Srs(SRS)
    
    return([SRS,IDs,Groups])         
