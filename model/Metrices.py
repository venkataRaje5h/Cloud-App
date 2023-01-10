from model.Authentication import AuthManagament
from model.Common import checking_name, server_path
import os


class MetricsManagement:

    def __init__(self):
        self.auth_obj = AuthManagament()

    def get_size_folder(self, folder):
        folder_size = 0
        images_in_folder = os.listdir(folder)
        try:
            images_in_folder.remove(".DS_Store")
        except:
            pass
        count = len(images_in_folder)
        os.chdir(folder)
        for image in images_in_folder:
            with open(image, 'rb') as f:
                folder_size += len(f.read())
        return [folder_size, count]

    def folder_metrics(self, authKey, folder_name):
        folder_name = checking_name(folder_name)
        email_check = self.auth_obj.get_user_email_from_authkey(authKey)
        if email_check is None:
            return -1  # authentication failure
        user_path = os.path.join(server_path, email_check)
        folder_path = os.path.join(user_path, folder_name)
        if os.path.exists(folder_path):
            folder_details = self.get_size_folder(folder_path)
            return folder_details
        else:
            return -2

    def user_metrics(self, authKey):
        email_check = self.auth_obj.get_user_email_from_authkey(authKey)
        if email_check is None:
            return -1  # authentication failure
        user_path = os.path.join(server_path, email_check)
        if os.path.exists(user_path):
            user_folder_list = os.listdir(user_path)
            try:
                user_folder_list.remove(".DS_Store")
            except:
                pass
            metrics_list = []
            for folder_name in user_folder_list:
                folder_path = os.path.join(user_path, folder_name)
                folder_details = self.get_size_folder(folder_path)
                folder_details.append(folder_name)
                metrics_list.append(folder_details)
            return metrics_list
        else:
            return -2
