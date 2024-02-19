"""
This script contains the unit tests for the Hotel class.

It utilizes the following modules:
- `unittest` for running the tests.
- `unittest.mock` for mocking standard output.
- `json` for encoding and decoding JSON data.
- `io` for handling input/output operations.
- `Hotel` from `booking.hotels.hotel` for testing the Hotel class.
"""
import unittest
import unittest.mock
import json
import io
from booking.hotels.hotel import Hotel


class TestHotel(unittest.TestCase):
    """
    Class to test the Hotel class.
    """

    def setUp(self):
        """
        setUp: Initializes a new Hotel object for each test.
        """
        self.hotel = Hotel("Test Hotel", 100, "Test Location")

    def test_hotel_initialization(self):
        """
        test_hotel_initialization: Tests the initialization of a Hotel object.
        """
        self.assertEqual(self.hotel.name, "Test Hotel")
        self.assertEqual(self.hotel.num_rooms, 100)
        self.assertEqual(self.hotel.ubication, "Test Location")

    def test_to_dict(self):
        """
        test_to_dict: Tests the to_dict method of a Hotel object.
        """
        expected_dict = {
            "name": self.hotel.name,
            "num_rooms": self.hotel.num_rooms,
            "ubication": self.hotel.ubication
        }
        self.assertEqual(self.hotel.to_dict(), expected_dict)

    def test_load_hotels(self):
        """
        test_load_hotels: Tests the load_hotels method of the Hotel class.
        """
        hotels = Hotel.load_hotels()
        self.assertIsInstance(hotels, list)

    def test_save_to_json(self):
        """
        test_save_to_json: Tests the save_to_json method of a Hotel object.
        """
        self.hotel.save_to_json()
        with open(Hotel.hotels_file, 'r', encoding='utf-8') as file:
            hotels = json.load(file)
        self.assertIn(self.hotel.to_dict(), hotels)
        Hotel.delete_hotel(self.hotel.name)

    def test_create_hotel_affirmative(self):
        """
        test_create_hotel_affirmative: Tests the create_hotel method of the
        Hotel class.
        """
        save_name = "Test Hotel"
        save_num_rooms = 100
        save_ubication = "Test Location"
        save_hotel = Hotel.create_hotel(save_name,
                                        save_num_rooms,
                                        save_ubication
                                        )
        hotels = Hotel.load_hotels()
        self.assertIn(save_hotel.to_dict(), hotels)
        Hotel.delete_hotel(save_hotel.name)

    def test_create_hotel_invalid_name(self):
        """
        test_create_hotel_invalid_name: Tests the create_hotel method
        with an invalid name.
        """
        invalid_name = 123
        invalid_num_rooms = 100
        invalid_ubication = "Test Location"
        invalid_hotel = Hotel.create_hotel(invalid_name,
                                           invalid_num_rooms,
                                           invalid_ubication
                                           )
        self.assertIsNone(invalid_hotel)

    def test_create_hotel_invalid_num_rooms(self):
        """
        test_create_hotel_invalid_num_rooms: Tests the create_hotel method
        with an invalid num_rooms.
        """
        invalid_name = "Test Hotel"
        invalid_num_rooms = "100"
        invalid_ubication = "Test Location"
        invalid_hotel = Hotel.create_hotel(invalid_name,
                                           invalid_num_rooms,
                                           invalid_ubication
                                           )
        self.assertIsNone(invalid_hotel)

    def test_create_hotel_invalid_ubication(self):
        """
        test_create_hotel_invalid_ubication: Tests the create_hotel method
        with an invalid ubication.
        """
        invalid_name = "Test Hotel"
        invalid_num_rooms = 100
        invalid_ubication = 123
        invalid_hotel = Hotel.create_hotel(invalid_name,
                                           invalid_num_rooms,
                                           invalid_ubication
                                           )
        self.assertIsNone(invalid_hotel)

    def test_delete_hotel_affirmative(self):
        """
        test_delete_hotel_affirmative: Tests the delete_hotel method of
        the Hotel class.
        """
        self.hotel.save_to_json()
        self.assertTrue(Hotel.delete_hotel(self.hotel.name))

    def test_delete_hotel_negative(self):
        """
        test_delete_hotel_negative: Tests the delete_hotel method with
        an invalid name.
        """
        self.hotel.save_to_json()
        self.assertFalse(Hotel.delete_hotel("Bad_Name"))
        Hotel.delete_hotel(self.hotel.name)

    def test_display_non_existing_hotel(self):
        """
        test_display_non_existing_hotel: Tests the display_hotel method
        with a non-existing name.
        """
        with unittest.mock.patch('sys.stdout',
                                 new=io.StringIO()) as fake_stdout:
            Hotel.display_hotel("Bad_Name")
            output = fake_stdout.getvalue().strip()
            self.assertEqual(output, "Hotel not found")

    def test_update_hotel(self):
        """
        test_update_hotel: Tests the update_hotel method of the Hotel class.
        """
        self.hotel.save_to_json()
        new_num_rooms = 200
        new_ubication = "New Location"
        self.assertTrue(Hotel.update_hotel(self.hotel.name,
                                           new_num_rooms,
                                           new_ubication
                                           ))
        hotels = Hotel.load_hotels()
        updated_hotel = next(
            (h for h in hotels if h["name"] == self.hotel.name),
            None
        )
        self.assertIsNotNone(updated_hotel)
        self.assertEqual(updated_hotel["num_rooms"], new_num_rooms)
        self.assertEqual(updated_hotel["ubication"], new_ubication)


if __name__ == '__main__':
    unittest.main()
