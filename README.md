Welcome to **isaikootu**!
=========================
This is _very early not even alpha_ python app, which can: 
 * index any directory for music files.
 * search the index.

Basic Usage:
------------
  *To index:*      
  
  
    
    $isaikootu index /home/tamizhgeek/Music
    
    
    
  *To search:*
  
    
    
    $isaikootu search album 'Mariyaan' 
    
    
    
  *For more options:*
  
    
    
    $isaikootu help [COMMAND]
    
    


Current State:
--------------
* Currently, this supports only a few filetypes such as mp3, avi, mkv, mp4, aac, ogg. 

* Regarding metadata, currently it supports only ID3 tags. XMP support is Work in Progress.



Installation:
-------------

* To install just extract this dir and type, 'python setup.py install'

* To run the tests type, 'python setup.py tests'

Misc:
-----
The index uses SQLite database and it is located under .isaikootu dir inside your home dir.

Thanks!
