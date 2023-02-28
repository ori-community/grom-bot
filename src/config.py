import os

SECURE = bool(os.environ.get('SECURE', True))
HOST = os.environ.get('HOST', 'wotw.orirando.com')
TOKEN = os.environ.get('TOKEN', False)
API_TOKEN = os.environ.get('API_TOKEN', '')

if not TOKEN:
    raise EnvironmentError("TOKEN environment variable not set")

if API_TOKEN == '':
    raise EnvironmentError("API_TOKEN environment variable not set")
