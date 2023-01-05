class User:
    memory = 500000000000

    def __init__(self, name, phone_no, user_email, user_password, country, used_memory, image_count):
        self.user_name = name
        self.phone_no = phone_no
        self.user_email = user_email
        self.user_password = user_password
        self.country = country
        self.used_memory = used_memory
        self.image_count = image_count


class Authorization:

    def __init__(self, token, email):
        self.auth_token = token
        self.user_email = email
