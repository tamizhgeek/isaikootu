from isaikootu.indexer import *
from isaikootu.models import MFile, ID3Tag

import os
import shutil


from playhouse.test_utils import test_database

test_db = SqliteDatabase(':memory:')


class TestIndexer():
    @classmethod
    def setup_class(cls):
        os.mkdir('/tmp/test_music_isaikootu')
        with open('/tmp/test_music_isaikootu/HipHop.mp3', 'w') as f:
            f.write('Junk')
        with open('/tmp/test_music_isaikootu/RockAndRoll.avi', 'w') as f:
            f.write('Junk')
        with open('/tmp/test_music_isaikootu/ignore.txt', 'w') as f:
            f.write('Junk')

    @classmethod
    def teardown_class(cls):
        shutil.rmtree('/tmp/test_music_isaikootu')
        
    def setup(self):
        with test_database(test_db, (MFile, ID3Tag)):
            self.indexer = Indexer('/tmp/test_music_isaikootu')
            self.indexer.index()
        
    def teardown(self):
        with test_database(test_db, (MFile, ID3Tag)):
            data = '%test_music_isaikootu%'
            mfile = MFile.select().where(MFile.fullpath ** data)
            for m in mfile:
                m.delete_instance()
            
    def test_index(self):
        with test_database(test_db, (MFile, ID3Tag)):
            MFile.select().where(MFile.name == 'ignore.txt').count == 0
            MFile.select().where(MFile.extension == 'mp3').count == 0
            MFile.select().where(MFile.name ** '%Rock%').count == 0
