import psycopg2
import os
import shutil
from PIL import Image
import io

from model.Authentication import AuthManagament
from model.Common import checking_name, server_path
from model.User import UserManagement


def connection():
    conn = psycopg2.connect(host="localhost", user="venkat-16321", password='', database='Cloud Apps')
    return conn


class ImageManagement:

    def __init__(self):
        self.user_obj = UserManagement()
        self.auth_obj = AuthManagament()

    def insert_image(self, image, folder_name, image_name, authKey):
        folder_name = checking_name(folder_name)
        image_name = checking_name(image_name)
        fetching_email = self.auth_obj.get_user_email_from_authkey(authKey)
        if fetching_email is None:
            return -1  # authentication failure
        user_path = os.path.join(server_path, fetching_email)
        folder_path = os.path.join(user_path, folder_name)
        if os.path.exists(folder_path):
            os.chdir(folder_path)
            bytearr = bytearray(image.file.read())
            photo = Image.open(io.BytesIO(bytearr))
            image_size = len(bytearr)
            if not os.path.exists(image_name):
                checking_space = self.user_obj.updating_user_memory(image_size, fetching_email, 1)
            else:
                checking_space = 1
            if checking_space > 0:
                photo.save(image_name)
                return image_size
            else:
                return -3
        else:
            return -2

    # def get_images_in_folder(self, authKey, folder_name):
    #     folder_name = checking_name(folder_name)
    #     email_check = self.auth_obj.get_user_email_from_authkey(authKey)
    #     if email_check is None:
    #         return -1  # authentication failure
    #     user_path = os.path.join(server_path, email_check)
    #     folder_path = os.path.join(user_path, folder_name)
    #     if os.path.exists(folder_path):
    #         user_folders = os.listdir(folder_path)
    #     else:
    #         return -2
    #     try:
    #         user_folders.remove(".DS_Store")
    #     except:
    #         pass
    #     return user_folders

    def get_images(self, authKey, folder_name, image_name):
        folder_name = checking_name(folder_name)
        email_check = self.auth_obj.get_user_email_from_authkey(authKey)
        if email_check is None:
            return -1  # authentication failure
        user_path = os.path.join(server_path, email_check)
        folder_path = os.path.join(user_path, folder_name)
        image_path = os.path.join(folder_path, image_name)
        if os.path.exists(folder_path):
            if os.path.exists(image_path):
                # image = open(image_path, 'rb')
                # bytearr = bytearray(image.read())
                # photo = Image.open(io.BytesIO(bytearr))
                return image_path
        else:
            return -2

    def delete_images_in_folder(self, authKey, folder_name, image_name):
        folder_name = checking_name(folder_name)
        image_name = checking_name(image_name)
        email_check = self.auth_obj.get_user_email_from_authkey(authKey)
        if email_check is None:
            return -1  # authentication failure
        user_path = os.path.join(server_path, email_check)
        folder_path = os.path.join(user_path, folder_name)
        image_path = os.path.join(folder_path, image_name)
        if os.path.exists(folder_path):
            if os.path.exists(image_path):
                image_size = os.stat(image_path).st_size * -1
                self.user_obj.updating_user_memory(image_size, email_check, -1)
                os.remove(image_path)
                return 1
            else:
                return -3
        else:
            return -2

    def move_image_another_folder(self, image_name, authKey, folder_name, another_folder_name):
        folder_name = checking_name(folder_name)
        another_folder_name = checking_name(another_folder_name)
        email_check = self.auth_obj.get_user_email_from_authkey(authKey)
        if email_check is None:
            return -1  # authentication failure
        user_path = os.path.join(server_path, email_check)
        folder_path = os.path.join(user_path, folder_name)
        another_folder_path = os.path.join(user_path, another_folder_name)
        image_path = os.path.join(folder_path, image_name)
        changing_image_path = os.path.join(another_folder_path, image_name)
        if os.path.exists(another_folder_path):
            if os.path.exists(folder_path):
                if os.path.exists(image_path):
                    shutil.move(image_path, changing_image_path)
                    return 1
                else:
                    return -3
            else:
                return -2
        else:
            return -4