import configparser

from ya_disk import YA_DISK

config = configparser.ConfigParser()
config.read("settings.ini")

TOKEN = config['TOKENS']['TOKEN']
TOKEN_YA = config['TOKENS']['TOKEN_YA']

if __name__ == "__main__":
    user_1 = YA_DISK(TOKEN_YA, TOKEN)
    user_1.create_holder()
    user_1.load_photos_and_writing_json()
