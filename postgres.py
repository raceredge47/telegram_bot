# Postgres connector
from psycopg2 import OperationalError
import psycopg2

# Time
from datetime import datetime

# Environment Variable
from decouple import config

# Uuid
import uuid


class Postgres:
    def __init__(self):
        self.con = None

    def conn(self):
        try:
            self.con = psycopg2.connect(
                    database=config('DATABASE'),
                    user=config('NAME'),
                    password=config('PASSWORD'),
                    host=config('HOST'),
                    port=config('PORT')
                )
            return self.con
        except OperationalError as Err:
            return Err


    def save(self, chat_id, username, first_name, last_name, photo, type, email):
        con = self.conn()
        cur = con.cursor()
        time = datetime.now()
        search_query = '''
                        SELECT id FROM USERS 
                        WHERE email=%s
                       '''
        cur.execute(search_query, [email])
        user_id = cur.fetchone()
        exists_query = '''
                       SELECT user_id FROM TELEGRAMS
                       WHERE user_id=%s
                       '''
        cur.execute(exists_query, [*user_id])
        row = cur.fetchall()
        if row:
            print('Exists')
        else:    
            insert_query = '''
                        INSERT INTO TELEGRAMS (id, created_at, updated_at, user_id, chat_id, 
                                            telegram_username, first_name, last_name, photo,
                                            type)
                        VALUES
                        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        '''
            data = [str(uuid.uuid4()), time, time, str(*user_id), 
                    chat_id, username, first_name, last_name, photo, type
                    ]
            cur.execute(insert_query, data)
            con.commit()


db = Postgres()