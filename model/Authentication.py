import random
import string
import time

from model.Common import connection


class AuthManagament:

    def __init__(self):
        self.conn = connection()
        self.my_cursor = self.conn.cursor()

    def insert_token(self, token, email, curr_time):
        query = "INSERT INTO public.auth_key (user_email, auth_token, expiry_time) VALUES (%s, %s, %s)"
        value = (email, token, curr_time,)
        self.my_cursor.execute(query, value)
        self.conn.commit()

    def get_tokens(self):
        query = "SELECT auth_token FROM auth_key"
        self.my_cursor.execute(query)
        result = []
        for token in self.my_cursor.fetchall():
            result.append(token[0])
        return result

    def generate_token(self, email):
        self.remove_tokens()
        token = ''.join(random.sample(string.hexdigits, int(16)))
        validity = round(time.time() * 1000) + (60 * 60 * 1000)
        tokens = self.get_tokens()
        while True:
            if token not in tokens:
                self.insert_token(token, email, validity)
                push = []
                push.append(token)
                push.append(validity)
                return push
            token = ''.join(random.sample(string.hexdigits, int(16)))

    def remove_tokens(self):
        curr_time = round(time.time() * 1000)
        query = "DELETE FROM auth_key where expiry_time <= %s"
        self.my_cursor.execute(query, (curr_time,))
        self.conn.commit()

    def get_user_email_from_authkey(self, auth_key):
        self.remove_tokens()
        query = "SELECT user_email FROM auth_key where auth_token = %s"
        value = (auth_key,)
        self.my_cursor.execute(query, value)
        result = self.my_cursor.fetchone()
        if result is not None:
            return result[0]
        return None