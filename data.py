import os.path

from joblib import Memory
from xbbg import blp

location = os.path.dirname(os.path.realpath(__file__)) + '/cachedir'
memory = Memory(location, verbose=0)
bdh = memory.cache(blp.bdh)
