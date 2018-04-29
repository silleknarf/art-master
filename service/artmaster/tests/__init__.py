import sys, os
path = os.path.dirname(__file__)
path = os.path.join(path, '../artmaster')
if path not in sys.path:
    sys.path.append(path)

import app
@app.app.errorhandler(Exception)
def handle_error(e):
    raise e