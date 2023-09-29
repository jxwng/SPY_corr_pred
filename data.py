from joblib import Memory
from xbbg import blp

location = './cachedir'
memory = Memory(location, verbose=0)
bdh = memory.cache(blp.bdh)
