import sqlite3
import unittest
from unittest.mock import patch, MagicMock
from DB.db_implementation import Activity_DB
from API.api_wrapper import ApiWrapper



class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.activity_entries = ['activity', 'type', 'participants', 'price', 'link', 'key', 'accessibility']
        cls.wrapper = ApiWrapper()

    def test_response(self):
        response: dict = self.wrapper.get_response()

        with patch('API.api_wrapper.requests') as mock_obj:
            activity = {'activity': 'Learn calligraphy', 'type': 'education', 'participants': 1, 'price': 0.1,
                        'link': '', 'key': '4565537', 'accessibility': 0.1}

            mock_get_resp = MagicMock()
            mock_get_resp.json.return_value = activity

            mock_obj.get.return_value = mock_get_resp

            response = self.wrapper.get_response()

            for key, value in response.items():
                with self.subTest(key):
                    self.assertEqual(value, activity[key])

    def test_bad_request(self):
        response = self.wrapper.get_response(type='nothing', participants=1000, price_max=10000, price_min=100000)
        self.assertEqual(response['error'], 'No activity found with the specified parameters')


class TestDB(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        self.activity = {'activity': 'Learn calligraphy', 'type': 'education', 'participants': 1, 'price': 0.1,
                         'link': '', 'key': '4565537', 'accessibility': 0.1}
        self.activity_incorrect = {'activity': 1, 'type': 2, 'participants': 1, 'price': 'safdsaf', 'link': '',
                                   'key': '4565537', 'accessibility': 0.1}

    def test_create_field(self):
        with patch('DB.db_implementation.sqlite3') as mock_obj:
            connect = MagicMock()
            cursor = MagicMock()

            connect.cursor.return_value = cursor
            cursor.execute.return_value = None
            mock_obj.connect.return_value = connect

            my_db = Activity_DB()
            my_db.connect()
            result = my_db.create_field(self.activity)

            self.assertEqual(result, self.activity)

    def test_latest_entries(self):
        with patch('DB.db_implementation.sqlite3') as mock_obj:
            table_name = (('activity',),
                          ('type',),
                          ('participants',),
                          ('price',),
                          ('link',),
                          ('key',),
                          ('accessibility',))

            fetchall = (
            ('Read a formal research', 'education', 1,0, 'https:google.com', '6706598', 0.1,),
            ('Read', 'charity', 2, 0, 'https:google.com', '6756598', 0.15 ),
            ('formal research', 'social', 2, 0, 'https:google.com', '6206598', 0.3),
            ('research', 'relaxation', 1, 0, 'https:google.com', '6306598', 0.2),
            ('research saf', 'education', 1, 0, 'https:google.com', '6406598', 0.25),
            )

            correct_response = 'activity -> research saf, type -> education, participants -> 1, price -> 0, link -> https:google.com, key -> 6406598, accessibility -> 0.25\n' \
                    'activity -> research, type -> relaxation, participants -> 1, price -> 0, link -> https:google.com, key -> 6306598, accessibility -> 0.2\n' \
                    'activity -> formal research, type -> social, participants -> 2, price -> 0, link -> https:google.com, key -> 6206598, accessibility -> 0.3\n' \
                    'activity -> Read, type -> charity, participants -> 2, price -> 0, link -> https:google.com, key -> 6756598, accessibility -> 0.15\n' \
                    'activity -> Read a formal research, type -> education, participants -> 1, price -> 0, link -> https:google.com, key -> 6706598, accessibility -> 0.1'


            connect = MagicMock()
            cursor = MagicMock()

            connect.cursor.return_value = cursor
            cursor.execute.return_value = None
            cursor.fetchall.return_value = fetchall
            cursor.description = table_name
            mock_obj.connect.return_value = connect

            my_db = Activity_DB()
            my_db.connect()
            result = my_db.get_latest_entries()

            self.assertEqual(result, correct_response)

    def test_db_error(self):
        with Activity_DB() as my_db:
            result = my_db.create_field(self.activity_incorrect)

        self.assertEqual(result, 'An error occurred while inserting into the database')
