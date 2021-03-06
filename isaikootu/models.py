import os
from peewee import *

if not os.path.exists(os.path.join(os.path.expanduser('~'),'.isaikootu')):
    os.mkdir(os.path.join(os.path.expanduser('~'),'.isaikootu'))

db = SqliteDatabase(os.path.join(os.path.expanduser('~'),'.isaikootu', 'isaikootu.db'))

class IsaiKootuModel(Model):
    class Meta:
        database = db

class MFile(IsaiKootuModel):
    name = CharField()
    fullpath = TextField()
    modtime = DateTimeField()
    dirpath = TextField()
    hashed = TextField()
    extension = CharField(choices = ['.mp3','.mp4','.oog','.aac','.avi','.mkv', '.m4a'])
    
class ID3Tag(IsaiKootuModel):
    mfile = ForeignKeyField(MFile)
    title = TextField(null = True)
    genre = TextField(null =  True)
    artist = TextField(null = True)
    album = TextField(null = True)
    length = DecimalField(null = True)
