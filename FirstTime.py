# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 21:05:21 2017

@author: chris


This will download the necessary files from Tatoeba. These files contain 
the relationsships between the different langauge sentences, the sentences with
audio, the user etc.

It will also download ffmpeg which is needed to handle the audio files and 
combine them. It will place the file in the needed folder
"""

import tarfile
import os
import re
import urllib.request
import subprocess

def Download_Tars():
    files = ['http://downloads.tatoeba.org/exports/sentences_detailed.tar.bz2',
             'http://downloads.tatoeba.org/exports/links.tar.bz2',
             'http://downloads.tatoeba.org/exports/sentences_with_audio.tar.bz2']
    
    folder = os.getcwd()
    
    
    for file in files:
        #gets the correct file extension
        name = re.split(r'/',file)[-1]
        filename = os.path.join(folder, name)
        urllib.request.urlretrieve(file,filename)
        
        tar=tarfile.open(filename)
        tar.extractall()
        tar.close()
        
        
        
'''
 this is a 'utility' used to install packages
 this script will download all of the packages that are needed for 
 this project
'''
import pip


def install(package):
    pip.main(['install', package])

packages = ['pydub','urllib.request','os','sys','numpy','pandas','random','sys','site','textstat','subprocess']

def Install_All():
    for package in packages:
        install(package)
        
        
'''
libav doesn't seem to work as well as ffmpeg so I am not using this.
I don't know how to edit this for ffmpeg the user need to do this manually        
def get_ffmpeg():
    
    folder = os.getcwd()
    
    
    #https://stackoverflow.com/questions/2208828/detect-64bit-os-windows-in-python
    def os_arch():
        os_arch = '32-bit'
        if os.name == 'nt':
            output = subprocess.check_output(['wmic', 'os', 'get', 'OSArchitecture'])
            os_arch = output.split()[1]
        else:
            output = subprocess.check_output(['uname', '-m'])
            if 'x86_64' in output:
                os_arch = '64-bit'
            else:
                os_arch = '32-bit'
        return os_arch

    
    
    
    if os_arch == '64-bit':
        url = r"http://builds.libav.org/windows/release-gpl/libav-0.8.17-win64.7z"
        filename = 'libav-64.7z'
    else:
        url = r"http://builds.libav.org/windows/release-gpl/libav-0.8.17-win32.7z"
        filename = 'libav-32.7z'
    
    filename = os.path.join(folder,filename)
    
    urllib.request.urlretrieve(url,filename)


print('what up')
get_ffmpeg()
'''

Install_All()
Download_Tars()

