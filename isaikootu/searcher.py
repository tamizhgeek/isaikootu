from models import *

import logging

class SearcherError(Exception): pass

class Searcher(object):
    def __init__(self):
        self.allowed_filters = ['title', 'album', 'artist', 'filetype', 'name']
        self.logger = logging.getLogger('isaikootu.searcher')

    ''' I am the main search utility. I get keywords and search criteria and
    do a search on appropiate fields.
    @param data: keywords to search
    @param ffilter: filter to apply for search, such as file extension
    @return res,count: list of matching mfile records.
                       returns [] when nothing found. None when search is not performed'''
    def search(self, data, ffilter = 'name'):
        if data is None or data == '':
            self.logger.warn("Nothing to search")
            return None

        if ffilter not in self.allowed_filters:
            raise SearcherError, "Invalid filter. Allowed filters are %s" % (',').join(self.allowed_filters)

        if ffilter == 'name':
            return self._part_of_name_search(data)
        elif ffilter in ('title', 'album', 'artist'):
            return self._metadata_search(data, ffilter)
        elif ffilter == 'filetype':
            return self._filetype_search(data)
            
    def _part_of_name_search(self, data):
        data = "%%%s%%" % data
        mfiles = MFile.select().where(MFile.fullpath ** data)
        return mfiles

    def _metadata_search(self, data, ffilter):
        data = "%%%s%%" % data
        mfiles = MFile.select().join(ID3Tag).where(eval('ID3Tag.'+ffilter) ** data)
        return mfiles
    
    def _filetype_search(self, data):
        data = "%%%s%%" %  data
        mfiles = MFile.select().where(MFile.extension ** data)
        return mfiles

