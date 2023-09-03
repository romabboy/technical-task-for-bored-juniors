import requests

class ApiWrapper:
    URL = 'https://www.boredapi.com/api/activity'
    def get_response(self, type=None, participants=None, price_min=None, price_max=None, accessibility_min=None, accessibility_max=None):
        params_dict = {
            'type': type,
            'participants': participants,
            'minprice': price_min,
            'maxprice': price_max,
            'minaccessibility': accessibility_min,
            'maxaccessibility': accessibility_max
        }

        params_dict = {key:value for (key,value) in params_dict.items() if value}
        response = requests.get(self.URL, params=params_dict).json()

        return response






