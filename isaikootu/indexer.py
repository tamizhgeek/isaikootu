import os
import logging
import datetime
import md5
import eyed3


from models import *

class Indexer(object):
    def __init__(self, root):
        self.logger = logging.getLogger('isaikootu.indexer')
        if os.path.exists(root):
            self.root = root
        else:
            raise IOError, "Invalid path given as root"
        
    # Crawl the filesytem and return a list of matching multimedia files.
    def _files_in_disk(self):
        self.logger.debug('Crawling the file system please wait...')
        file_list = []
        for root, subfolders, files in os.walk(self.root):
            for ffile in files:
                if os.path.splitext(ffile)[1] in MFile.extension.choices:
                    file_list.append(os.path.abspath(os.path.join(root,ffile)))
        self.logger.debug('Done crawling!')
        return file_list
    
    # List of files which are in index
    def _files_in_index(self):
        return [x.fullpath for x in MFile.select()]

    # Add a newly found file to index
    def _add_file(self, f):
        fname = os.path.abspath(os.path.join(self.root, f))
        m = MFile()
        m.name = os.path.basename(fname)
        m.fullpath = fname
        m.modtime = datetime.datetime.fromtimestamp(os.path.getmtime(fname))
        m.dirpath = os.path.dirname(fname)
        m.hashed = md5.new(fname).hexdigest()
        m.extension = os.path.splitext(f)[1]
        m.save()
        # Try extracting ID3 tags.
        self._extract_id3(fname, m)

    def _extract_id3(self, fname, mfile):
        self.logger.debug("Trying to extract ID3 data for %s" % mfile)
        try:
            f = eyed3.load(fname)
        except Exception as err:
            self.logger.error("Error occurred : %s",err)
            return
        id3 = ID3Tag()
        id3.mfile = mfile
        data_found = False
        if f is None:
            return 
        if f.tag is not None:
            id3.title = f.tag.title
            id3.album = f.tag.album
            id3.artist = f.tag.artist
            data_found = True
        if f.info is not None:
            id3.length = f.info.time_secs
            data_found = True
        if data_found:
            id3.save()
            return id3
        
    # Remove a dead file from index.
    def _remove_file(self, f):
        mfile = MFile.get(MFile.fullpath == f) 
        mfile.delete_instance()

    ''' I am the main index utility. I will crawl the the filesytem and index files.
    
    I use a not so intelligent method to do diff indexing. That is as follows.
    I first make of list of matching files in the filesytem, irrespective of whether they
    indexed or not say 'l1'. Then I make a list of files already in index 
    from the database say 'l2'.
    I find a diff of them : 
    (l1 - l2) gives me the files that are needed to be put in index.
    (l2 - l1) gives me the files which are dead and need to be removed from index
    
    Right now, I am kind of dumb and detect only filesystem changes. If there are changes
    to multimedia metadata such as ID3 tags, they aren't detected automatically for reindexing :(
    '''
    def index(self):
        existing_index = self._files_in_index()
        updated_index = self._files_in_disk()
        s = set(existing_index)
        newfiles = [x for x in updated_index if x not in s]
        s = set(updated_index)
        deleted = [x for x in existing_index if x not in s]

        for f in newfiles:
            self._add_file(f)
            
        for f in deleted:
            self._remove_file(f)
        
    
