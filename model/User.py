from model.Common import connection, server_path
from model.model_classes import User
import os
import shutil


class UserManagement:

    def __init__(self):
        self.conn = connection()
        self.my_cursor = self.conn.cursor()

    def insert_user(self, user_email, phone_number, password, country, user_name):
        query = "INSERT INTO public.app_user (user_email, phone_number, password, country, used_memory, user_name, image_count) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        value = (user_email, phone_number, password, country, 0, user_name, 0,)
        try:
            self.my_cursor.execute(query, value)
            self.conn.commit()
        except Exception as e:
            # print(e)
            return -1
        if self.my_cursor.rowcount > 0:
            try:
                path = os.path.join(server_path, user_email)
                os.makedirs(path)
            except Exception as e:
                pass
                # print(e)
                # return -2
        return self.my_cursor.rowcount

    def get_User(self, email):
        query = "SELECT * FROM app_user where user_email = %s"
        value = (email,)
        self.my_cursor.execute(query, value)
        result = self.my_cursor.fetchall()
        try:
            user = User(name=result[0][6], phone_no=result[0][1], user_email=result[0][0], user_password=result[0][2],
                        used_memory=result[0][5], country=result[0][3], image_count=result[0][7])
        except Exception:
            return None
        return user

    def update_user(self, email, password, user_name, phone_num):
        query = "UPDATE public.app_user SET  phone_number = %s, user_name=%s, password=%s where user_email = %s"
        values = (phone_num, user_name, password, email)
        self.my_cursor.execute(query, values)
        self.conn.commit()
        return self.my_cursor.rowcount

    def delete_user(self, email, password):
        query = "DELETE FROM app_user where user_email = %s and password = %s"
        value = (email, password)
        self.my_cursor.execute(query, value)
        self.conn.commit()
        if self.my_cursor.rowcount > 0:
            path = os.path.join(server_path, email)
            if os.path.exists(path):
                shutil.rmtree(path)
        return self.my_cursor.rowcount

    def updating_user_memory(self, image_size, email, count):
        conn = connection()
        my_cursor = conn.cursor()
        user = self.get_User(email)
        memory = user.used_memory + int(image_size)
        if memory <= user.memory:
            query = "UPDATE public.app_user SET used_memory = %s, image_count = %s where user_email = %s"
            values = (memory, user.image_count + count, email,)
            my_cursor.execute(query, values)
            conn.commit()
        # my_cursor.close()
        # conn.close()
        return my_cursor.rowcount