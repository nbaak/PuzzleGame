
import os
import pathlib
import secret_service

ip = '127.0.0.1'
port = 5000

THIS_PATH = pathlib.Path(__file__).parent.resolve()
SECRET_FILE = os.path.join(THIS_PATH, 'app.secret')
secret = secret_service.get_secret(SECRET_FILE)

