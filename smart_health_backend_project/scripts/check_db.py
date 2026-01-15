import os
import traceback
import psycopg

host = os.getenv('DATABASE_HOST', 'localhost')
port = os.getenv('DATABASE_PORT', '5432')
user = os.getenv('DATABASE_USER', 'postgres')
password = os.getenv('DATABASE_PASSWORD', '')
dbname = os.getenv('DATABASE_NAME', 'smart_health_dev')

print('Attempting connection with:')
print(f' host={host} port={port} user={user} dbname={dbname}')

try:
    conn = psycopg.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
        connect_timeout=5
    )
    print('Connected successfully')
    conn.close()
except Exception as e:
    print('Connection failed:')
    traceback.print_exc()
