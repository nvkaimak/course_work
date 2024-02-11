import datetime
import json

import requests
from tqdm import tqdm

from user_vk import USER_VK


class YA_DISK(USER_VK):
    BASE_URL_YA = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token_ya, token, owner_id=input('Enter id or username: ')):
        super().__init__(token, owner_id)
        self.token_ya = token_ya

    def common_params_ya(self):
        return {
            'path': f'{self.owner_id}'
        }

    def common_headers(self):
        return {
            'Authorization': f'OAuth {self.token_ya}'
        }

    def create_holder(self):
        params = self.common_params_ya()
        headers = self.common_headers()
        response = requests.put(self.BASE_URL_YA, params=params, headers=headers)
        return response

    def load_photos(self, count_photos=int(input('Enter count photos: '))):
        headers = self.common_headers()
        params = self.common_params_ya()
        photos = list(self.get_url_photos().items())[:count_photos]
        load_json = {}
        for url, likes in tqdm(photos):
            params['path'] = f'{self.owner_id}/{likes}'
            params['url'] = url
            response = requests.post(f'{self.BASE_URL_YA}/upload', params=params, headers=headers)
            if response.status_code == 202:
                load_json[likes] = {'link': url, 'date_load': f'{datetime.datetime.now()}'}

        return json.dumps(load_json)

    def load_photos_and_writing_json(self):
        json_data = self.load_photos()
        with open("load.json", "w") as f:
            f.write(json_data)
