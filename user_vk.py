from datetime import datetime

import requests

class USER_VK(object):
    BASE_URL = 'https://api.vk.com/method/'

    def __init__(self, token, owner_id):
        self.token = token
        self.owner_id = owner_id

    def common_params_vk(self):
        return {
            'access_token': self.token,
            'v': '5.131',
        }

    def get_id(self):
        params = self.common_params_vk()
        params['user_ids'] = self.owner_id
        response = requests.get(self.BASE_URL + 'users.get', params=params).json()
        return ((response['response'])[0])['id']

    def get_photos(self):
        if self.owner_id.isdigit():
            self.owner_id = int(self.owner_id)
        else:
            self.owner_id = self.get_id(self.owner_id)
        params = self.common_params_vk()
        params['owner_id'] = self.owner_id
        params['album_id'] = 'profile',
        params['extended'] = 1
        response = requests.get(self.BASE_URL + 'photos.get', params)
        return response.json()

    def get_url_photos(self):
        photos = self.get_photos()
        dict_photos = {}
        for info_photo in photos.get('response').get('items'):
            count_likes = info_photo.get('likes').get('count')
            for photo in info_photo.get('sizes'):
                if photo.get('type') == 'x':
                    if count_likes not in dict_photos.values():
                        dict_photos[photo.get('url')] = count_likes
                    else:
                        dict_photos[photo.get('url')] = str(count_likes) + ' ' + datetime.utcfromtimestamp(
                            info_photo.get('date')).strftime('%Y-%m-%d %H:%M')
        return dict_photos
