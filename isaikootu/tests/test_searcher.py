import datetime
import os

from isaikootu.models import MFile, ID3Tag
from isaikootu.searcher import *

from playhouse.test_utils import test_database

test_db = SqliteDatabase(':memory:')


class TestSearcher():
    def setuptestdata(self):
        self.m1 = MFile.create(name='rap_song.mp3', fullpath='/tmp/rap_song.mp3', dirpath = '/tmp/', hashed="somerandomvalue", modtime = datetime.datetime.today(), extension = '.mp3')
        self.m2 = MFile.create(name='rap_song_tamil.mp3', fullpath='/tmp/rap_song_tamil.mp3', dirpath = '/tmp/', hashed="somerandomvalue", modtime = datetime.datetime.today(), extension = '.mp3')
        self.m3 = MFile.create(name='dexter.avi', fullpath='/tmp/dexter.avi', dirpath = '/tmp/', hashed="somerandomvalue", modtime = datetime.datetime.today(), extension = '.avi')
        self.m4 = MFile.create(name='jazz_song_english.mp4', fullpath='/tmp/jazz_song_english.mp4', dirpath = '/tmp/', hashed="somerandomvalue", modtime = datetime.datetime.today(), extension = '.mp4')
        ID3Tag.create(mfile = self.m2, title = "Rap Song", album = "Hip Hop Tamizha")
        self.searcher = Searcher()

    def teardowntestdata(self):
        self.m1.delete_instance()
        self.m2.delete_instance()
        self.m3.delete_instance()
        self.m4.delete_instance()

    def test_searcher(self):
        with test_database(test_db, (MFile, ID3Tag)):
            self.setuptestdata()
            assert self.searcher.search('rap_song_tamil').count() == 1
            assert self.searcher.search('rap_song').count() == 2
            assert self.searcher.search('raja', 'artist').count() == 0
            assert self.searcher.search('Hip', 'album').count() == 1
            assert self.searcher.search('mp3').count() == 2
            assert self.searcher.search('mp4').count() == 1
            assert self.searcher.search('avi', 'filetype').count() == 1
            self.teardowntestdata()
