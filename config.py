from dotenv import load_dotenv

import os


load_dotenv()

DB_HOST=os.environ.get('DB_HOST')
DB_PORT=os.environ.get('DB_PORT')
DB_NAME=os.environ.get('DB_NAME')
DB_USER=os.environ.get('DB_USER')
DB_PASS=os.environ.get('DB_PASS')
USER_SECRET=os.environ.get('USER_SECRET')
USER_MENEGER_SECRET=os.environ.get('USER_MENEGER_SECRET')