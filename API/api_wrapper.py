import requests

class ApiWrapper:
    allowed_values = ['activity', 'type', 'participants', 'price', 'link', 'key', 'accessibility']
    URL = 'https://www.boredapi.com/api/activity'

    def get_response(self, **kwargs):
        result = None

        if not kwargs:
            result = requests.get(self.URL).json()
        else:
            difference = set(kwargs) - set(self.allowed_values)

            if difference: result = f'You have passed wrong params -> {difference}'
            else: result = requests.get(self.URL,params=kwargs).json()

        return result


