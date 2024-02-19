"""
This script utilizes the following modules:
- `json` for encoding and decoding JSON data.
- `os` for interacting with the operating system.
"""
import json
import os


class Hotel:
    """
    Class to represent a hotel.

    Attributes:
        data_folder (str): The path of the data folder.
        hotels_file (str): The path of the JSON file that stores the hotels.
    """
    data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               "../data"))
    hotels_file = os.path.join(data_folder, "hotels.json")

    def __init__(self, name, num_rooms, ubication):
        """
        __init__: Initializes a new hotel object.
        """
        self.name = name
        self.num_rooms = num_rooms
        self.ubication = ubication

    def to_dict(self):
        """
        to_dict: Converts the hotel object into a dictionary.
        """
        return {
            "name": self.name,
            "num_rooms": self.num_rooms,
            "ubication": self.ubication
        }

    @classmethod
    def load_hotels(cls):
        """
        load_hotels: Loads the hotels from the JSON file.
        """
        if not os.path.exists(cls.hotels_file):
            return []
        with open(cls.hotels_file, 'r', encoding="utf-8") as file:
            return json.load(file)

    def save_to_json(self):
        """
        save_to_json: Saves the hotel to the JSON file.
        """
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

        hotels = self.load_hotels()
        hotels.append(self.to_dict())
        with open(self.hotels_file, 'w', encoding="utf-8") as file:
            json.dump(hotels, file, indent=4)

    @classmethod
    def create_hotel(cls, name, num_rooms, ubication):
        """
        create_hotel: Creates a new hotel and saves it to the JSON file.
        """
        try:
            if not isinstance(name, str):
                raise ValueError("name must be a string")
            if not isinstance(num_rooms, int):
                raise ValueError("num_rooms must be a string")
            if not isinstance(ubication, str):
                raise ValueError("ubication must be a string")
            hotel = Hotel(name, num_rooms, ubication)
            hotel.save_to_json()
            return hotel
        except ValueError as e:
            print(f"Error create hotel: {e}")
            return None

    @classmethod
    def delete_hotel(cls, name):
        """
        delete_hotel: Deletes a hotel from the JSON file.
        """
        confirmed = False
        hotels = cls.load_hotels()
        for hotel in hotels:
            if hotel["name"] == name:
                hotels.remove(hotel)
                confirmed = True
                break
        with open(cls.hotels_file, 'w', encoding="utf-8") as file:
            json.dump(hotels, file, indent=4)
        return confirmed

    @classmethod
    def display_hotel(cls, name):
        """
        display_hotel: Displays the information of a hotel.
        """
        founded = False
        hotels = cls.load_hotels()
        for hotel in hotels:
            if hotel["name"] == name:
                founded = True
                print(hotel)
                break
        if not founded:
            print("Hotel not found")
        return founded

    @classmethod
    def update_hotel(cls, name, new_num_rooms=None, new_ubication=None):
        """
        update_hotel: Updates the information of a hotel.
        """
        updated = False
        hotels = cls.load_hotels()
        for hotel in hotels:
            if hotel["name"] == name:
                updated = True
                if new_num_rooms:
                    hotel["num_rooms"] = new_num_rooms
                if new_ubication:
                    hotel["ubication"] = new_ubication
                break
        with open(cls.hotels_file, 'w', encoding="utf-8") as file:
            json.dump(hotels, file, indent=4)
        if not updated:
            print("Hotel not found")
        return updated
