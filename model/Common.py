import psycopg2

server_path = "/Users/venkat-16321/Desktop/Cloud"


def connection():
    conn = psycopg2.connect(host="localhost", user="venkat-16321", password='', database='Cloud Apps')
    return conn


def checking_name(name):
    valid_name = ""
    for ch in name:
        if ch == " ":
            valid_name += '_'
        else:
            valid_name += ch
    return valid_name


