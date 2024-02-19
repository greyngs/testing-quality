"""
This script utilizes the following modules:
- `json` for encoding and decoding JSON data.
- `os` for interacting with the operating system.
- `uuid` for generating UUIDs.
"""
import json
import os
import uuid


class Reservation:
    """
    Class to represent a reservation.

    Attributes:
        data_folder (str): The path of the data folder.
        reservations_file (str): The path of the JSON file
        that stores the reservations.
    """
    data_folder = "../data"
    reservations_file = os.path.join(data_folder, "reservations.json")

    def __init__(self, customer_id, hotel_name, room):
        """
        __init__: Initializes a new reservation object.
        """
        self.reservation_code = str(uuid.uuid4())
        self.customer_id = customer_id
        self.hotel_name = hotel_name
        self.room = room
        self.active = True

    def to_dict(self):
        """
        to_dict: Converts the reservation object into a dictionary.
        """
        return {
            "reservation_code": self.reservation_code,
            "customer_id": self.customer_id,
            "hotel_name": self.hotel_name,
            "room": self.room,
            "active": self.active
        }

    @classmethod
    def load_reservations(cls):
        """
        load_reservations: Loads the reservations from the JSON file.
        """
        if not os.path.exists(cls.reservations_file):
            return []
        with open(cls.reservations_file, 'r', encoding="utf-8") as file:
            return json.load(file)

    def save_to_json(self):
        """
        save_to_json: Saves the reservation to the JSON file.
        """
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

        reservations = self.load_reservations()
        reservations.append(self.to_dict())
        with open(self.reservations_file, 'w', encoding="utf-8") as file:
            json.dump(reservations, file, indent=4)

    @classmethod
    def create_reservation(cls, customer_id, hotel_name, room):
        """
        create_reservation: Creates a new reservation and saves
        it to the JSON file.
        """
        try:
            if not isinstance(customer_id, str):
                raise ValueError("customer_id must be a string")
            if not isinstance(hotel_name, str):
                raise ValueError("hotel_name must be a string")
            if not isinstance(room, str):
                raise ValueError("room must be a string")
            reservation = Reservation(customer_id, hotel_name, room)
            reservation.save_to_json()
            return reservation
        except ValueError as e:
            print(f"Error create reservation: {e}")
            return None

    @classmethod
    def cancel_reservation(cls, reservation_code):
        """
        cancel_reservation: Cancels a reservation and updates
        its status in the JSON file.
        """
        confirmed = False
        reservations = cls.load_reservations()
        for reservation in reservations:
            if reservation["reservation_code"] == reservation_code:
                confirmed = True
                reservation["active"] = False
                with open(cls.reservations_file,
                          'w',
                          encoding="utf-8") as file:
                    json.dump(reservations, file, indent=4)
        return confirmed

    @classmethod
    def delete_reservation(cls, reservation_code):
        """
        delete_reservation: Deletes a reservation from the JSON file.
        """
        confirmed = False
        reservations = cls.load_reservations()
        for reservation in reservations:
            if reservation["reservation_code"] == reservation_code:
                reservations.remove(reservation)
                confirmed = True
                break
        with open(cls.reservations_file, 'w', encoding="utf-8") as file:
            json.dump(reservations, file, indent=4)
        return confirmed
