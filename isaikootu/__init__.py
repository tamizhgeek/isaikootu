from models import *
from searcher import *
from indexer  import *

db.connect()
try:
    MFile.create_table()
except Exception:
    pass

try:
    ID3Tag.create_table()
except Exception:
    pass


