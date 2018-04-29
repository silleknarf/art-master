import sys, os
path = os.path.dirname(__file__)
path = os.path.join(path, '../artmaster')
if path not in sys.path:
    sys.path.append(path)