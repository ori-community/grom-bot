import os

SECURE = bool(os.environ.get('SECURE', True))
HOST = os.environ.get('HOST', 'wotw.orirando.com')
TOKEN = os.environ.get('TOKEN', False)

if not TOKEN:
    raise EnvironmentError("TOKEN environment variable not set")
