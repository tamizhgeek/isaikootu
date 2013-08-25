import os
import datetime
import md5
import eyed3
from models import *

class Indexer(object):
    def __init__(self, root):
        if os.path.exists(root):
            self.root = root
        else:
            raise IOError, "Invalid path given as root"
        
    def _files_in_disk(self):
        file_list = []
        for root, subfolders, files in os.walk(self.root):
            for ffile in files:
                if os.path.splitext(ffile)[1] in MFile.extension.choices:
                    file_list.append(os.path.abspath(os.path.join(root,ffile)))
        return file_list
    
    def _files_in_index(self):
        return [x.fullpath for x in MFile.select()]

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
        self._extract_id3(fname, m)

    def _extract_id3(self, fname, mfile):
        print fname
        try:
            f = eyed3.load(fname)
        except Exception, err:
            print("Error occurred : %s",err)
            return
        id3 = ID3Tag()
        id3.mfile = mfile
        data_found = False
        if f is None:
            return 
        print f.tag
        if f.tag is not None:
            id3.title = f.tag.title
            id3.album = f.tag.album
            id3.artist = f.tag.artist
            data_found = True
        if f.info is not None:
            id3.length = f.info.time_secs
            data_found = True
        if data_found:
            print id3
            id3.save()
            return id3
        
    def _remove_file(self, f):
        mfile = MFile.get(MFile.fullpath == f) 
        mfile.delete_instance()
    
    def index(self):
        existing_index = self._files_in_index()
        updated_index = self._files_in_disk()
        print existing_index
        print updated_index
        s = set(existing_index)
        newfiles = [x for x in updated_index if x not in s]
        s = set(updated_index)
        deleted = [x for x in existing_index if x not in s]

        for f in newfiles:
            self._add_file(f)
            
        for f in deleted:
            self._remove_file(f)
        
    
