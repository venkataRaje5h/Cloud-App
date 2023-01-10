import os
import shutil

from model.Authentication import AuthManagament
from model.Common import checking_name, server_path


class FolderManagement:

    def __init__(self):
        self.auth_obj = AuthManagament()

    def insert_folder(self, folder_name, auth_key):
        folder_name = checking_name(folder_name)
        email_check = self.auth_obj.get_user_email_from_authkey(auth_key)
        if email_check is None:
            return -1  # authentication failure
        user_path = os.path.join(server_path, email_check)
        folder_path = os.path.join(user_path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        else:
            return -2

    def delete_folder(self, folder_name, auth_key):
        folder_name = checking_name(folder_name)
        email_check = self.auth_obj.get_user_email_from_authkey(auth_key)
        if email_check is None:
            return -1  # authentication failure
        user_path = os.path.join(server_path, email_check)
        folder_path = os.path.join(user_path, folder_name)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        else:
            return -2

    def get_folder(self, auth_key):
        email_check = self.auth_obj.get_user_email_from_authkey(auth_key)
        if email_check is None:
            return -1  # authentication failure
        user_path = os.path.join(server_path, email_check)
        user_folders = os.listdir(user_path)
        try:
            user_folders.remove(".DS_Store")
        except:
            pass
        return user_folders

    def update_folder(self, old_folder_name, new_folder_name, authKey):
        old_folder_name = checking_name(old_folder_name)
        new_folder_name = checking_name(new_folder_name)
        email_check = self.auth_obj.get_user_email_from_authkey(authKey)
        if email_check is None:
            return -1  # authentication failure
        user_path = os.path.join(server_path, email_check)
        folder_path = os.path.join(user_path, old_folder_name)
        replacing_path = os.path.join(user_path, new_folder_name)
        if os.path.exists(folder_path):
            if not os.path.exists(replacing_path):
                os.replace(folder_path, replacing_path)
            else:
                return -3
        else:
            return -2