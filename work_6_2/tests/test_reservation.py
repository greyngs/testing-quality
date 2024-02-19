"""
This script contains the unit tests for the Reservation class.

It utilizes the following modules:
- `unittest` for running the tests.
- `unittest.mock` for mocking standard output.
- `json` for encoding and decoding JSON data.
- `Reservation` from `booking.reservations.reservation` for
   testing the Reservation class.
"""
import unittest
import unittest.mock
import json
from booking.reservations.reservation import Reservation


class TestReservation(unittest.TestCase):
    """
    Class to test the Reservation class.
    """

    def setUp(self):
        """
        setUp: Initializes a new Reservation object for each test.
        """
        self.reservation = Reservation("123", "Test Hotel", "Test Room")

    def test_reservation_initialization(self):
        """
        test_reservation_initialization: Tests the initialization of a
        Reservation object.
        """
        self.assertIsNotNone(self.reservation.reservation_code)
        self.assertEqual(self.reservation.customer_id, "123")
        self.assertEqual(self.reservation.hotel_name, "Test Hotel")
        self.assertEqual(self.reservation.room, "Test Room")
        self.assertTrue(self.reservation.active)

    def test_to_dict(self):
        """
        test_to_dict: Tests the to_dict method of a Reservation object.
        """
        expected_dict = {
            "reservation_code": self.reservation.reservation_code,
            "customer_id": self.reservation.customer_id,
            "hotel_name": self.reservation.hotel_name,
            "room": self.reservation.room,
            "active": self.reservation.active
        }
        self.assertEqual(self.reservation.to_dict(), expected_dict)

    def test_load_reservations(self):
        """
        test_load_reservations: Tests the load_reservations method of
        the Reservation class.
        """
        reservations = Reservation.load_reservations()
        self.assertIsInstance(reservations, list)

    def test_save_to_json(self):
        """
        test_save_to_json: Tests the save_to_json method of a Reservation
        object.
        """
        self.reservation.save_to_json()
        with open(Reservation.reservations_file,
                  'r',
                  encoding='utf-8') as file:
            reservations = json.load(file)
        self.assertIn(self.reservation.to_dict(), reservations)
        Reservation.delete_reservation(self.reservation.reservation_code)

    def test_create_reservation_affirmative(self):
        """
        test_create_reservation_affirmative: Tests the create_reservation
        method of the Reservation class.
        """
        save_customer_id = "123"
        save_hotel_name = "Test Hotel"
        save_room = "2B"
        save_reservation = Reservation.create_reservation(save_customer_id,
                                                          save_hotel_name,
                                                          save_room)
        reservations = Reservation.load_reservations()
        self.assertIn(save_reservation.to_dict(), reservations)
        Reservation.delete_reservation(save_reservation.reservation_code)

    def test_create_reservation_invalid_customer_id(self):
        """
        test_create_reservation_invalid_customer_id: Tests the
        create_reservation method with an invalid customer_id.
        """
        invalid_customer_id = 123
        invalid_hotel_name = "Test Hotel"
        invalid_room = "2B"
        invalid_reservation = Reservation.create_reservation(
            invalid_customer_id,
            invalid_hotel_name,
            invalid_room)
        self.assertIsNone(invalid_reservation)

    def test_create_reservation_invalid_hotel_name(self):
        """
        test_create_reservation_invalid_hotel_name: Tests the
        create_reservation method with an invalid hotel_name.
        """
        invalid_customer_id = "123"
        invalid_hotel_name = 123
        invalid_room = "2B"
        invalid_reservation = Reservation.create_reservation(
            invalid_customer_id,
            invalid_hotel_name,
            invalid_room)
        self.assertIsNone(invalid_reservation)

    def test_create_reservation_invalid_room(self):
        """
        test_create_reservation_invalid_room: Tests the create_reservation
        method with an invalid room.
        """
        invalid_customer_id = "123"
        invalid_hotel_name = "Test Hotel"
        invalid_room = 22
        invalid_reservation = Reservation.create_reservation(
            invalid_customer_id,
            invalid_hotel_name,
            invalid_room)
        self.assertIsNone(invalid_reservation)

    def test_cancel_reservation_affirmative(self):
        """
        test_cancel_reservation_affirmative: Tests the cancel_reservation
        method of the Reservation class.
        """
        self.reservation.save_to_json()
        self.assertTrue(Reservation.cancel_reservation(
            self.reservation.reservation_code))
        Reservation.delete_reservation(self.reservation.reservation_code)

    def test_cancel_reservation_negative(self):
        """
        test_cancel_reservation_negative: Tests the cancel_reservation
        method with an invalid reservation_code.
        """
        self.reservation.save_to_json()
        self.assertFalse(Reservation.cancel_reservation("Bad_Code"))
        Reservation.delete_reservation(self.reservation.reservation_code)

    def test_delete_reservation_affirmative(self):
        """
        test_delete_reservation_affirmative: Tests the delete_reservation
        method of the Reservation class.
        """
        self.reservation.save_to_json()
        self.assertTrue(Reservation.delete_reservation(
            self.reservation.reservation_code))

    def test_delete_reservation_negative(self):
        """
        test_delete_reservation_negative: Tests the delete_reservation method
        with an invalid reservation_code.
        """
        self.reservation.save_to_json()
        self.assertFalse(Reservation.delete_reservation("Bad_Code"))
        Reservation.delete_reservation(self.reservation.reservation_code)


if __name__ == '__main__':
    unittest.main()
