import logging
import os
import sys

from peewee import SqliteDatabase, PostgresqlDatabase

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

if not os.getenv('POSTGRES_DB_NAME'):
    logger.warning('[DB] using sqlite')
    db = SqliteDatabase('quiz.db')
else:
    logger.info('[DB] Connected to postgresql')
    db_name = os.getenv('POSTGRES_DB_NAME')
    db_user = os.getenv('POSTGRES_DB_USER')
    db_pass = os.getenv('POSTGRES_DB_PASS')
    db_host = os.getenv('POSTGRES_DB_HOST')
    db_port = int(os.getenv('POSTGRES_DB_PORT', 5432))
    db = PostgresqlDatabase(db_name, user=db_user, password=db_pass, host=db_host, port=db_port)

token_length = 64

site_host = os.getenv('APP_SITE_HOST')

# ---- SOCIAL NETWORKS CREDENTIALS ---- #
vk_client_id = os.getenv('VK_CLIENT_ID')
vk_client_secret = os.getenv('VK_CLIENT_SECRET')

fb_client_id = os.getenv('FB_CLIENT_ID')
fb_client_secret = os.getenv('FB_CLIENT_SECRET')

google_client_id = os.getenv('GOOGLE_CLIENT_ID')
google_client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
# ---- END OF CREDENTIALS ---- #
