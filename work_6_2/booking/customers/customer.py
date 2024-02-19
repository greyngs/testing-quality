"""
This script utilizes the following modules:
- `json` for encoding and decoding JSON data.
- `os` for interacting with the operating system.
"""
import json
import os


class Customer:
    """
    Class to represent a customer.

    Attributes:
        data_folder (str): The path of the data folder.
        customers_file (str): The path of the JSON file
        that stores the customers.
    """

    data_folder = os.path.abspath(os.path.join
                                  (os.path.dirname(__file__), "../data"))
    customers_file = os.path.join(data_folder, "customers.json")

    def __init__(self, customer_id, name, phone_number):
        """
        __init__: Initializes a new customer object.
        """
        self.customer_id = customer_id
        self.name = name
        self.phone_number = phone_number

    def to_dict(self):
        """
        to_dict: Converts the customer object into a dictionary.
        """
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "phone_number": self.phone_number
        }

    @classmethod
    def load_customers(cls):
        """
        load_customers: Loads the customers from the JSON file.
        """
        if not os.path.exists(cls.customers_file):
            return []
        with open(cls.customers_file, 'r', encoding="utf-8") as file:
            return json.load(file)

    def save_to_json(self):
        """
        save_to_json: Saves the customer to the JSON file.
        """
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        customers = self.load_customers()
        customers.append(self.to_dict())
        with open(self.customers_file, 'w', encoding="utf-8") as file:
            json.dump(customers, file, indent=4)

    @classmethod
    def create_customer(cls, customer_id, name, phone_number):
        """
        create_customer: Creates a new customer and saves it to the JSON file.
        """
        try:
            if not isinstance(customer_id, str):
                raise ValueError("customer_id must be a string")
            if not isinstance(name, str):
                raise ValueError("name must be a string")
            if not isinstance(phone_number, str):
                raise ValueError("phone_number must be a string")
            customer = Customer(customer_id, name, phone_number)
            customer.save_to_json()
            return customer
        except ValueError as e:
            print(f"Error create customer: {e}")
            return None

    @classmethod
    def delete_customer(cls, customer_id):
        """
        delete_customer: Deletes a customer from the JSON file.
        """
        confirmed = False
        customers = cls.load_customers()
        for customer in customers:
            if customer["customer_id"] == customer_id:
                customers.remove(customer)
                confirmed = True
                break
        with open(cls.customers_file, 'w', encoding="utf-8") as file:
            json.dump(customers, file, indent=4)
        return confirmed

    @classmethod
    def display_customer(cls, customer_id):
        """
        display_customer: Displays the information of a customer.
        """
        founded = False
        customers = cls.load_customers()
        for customer in customers:
            if customer["customer_id"] == customer_id:
                founded = True
                print(customer)
                break
        if not founded:
            print("Customer not found")
        return founded

    @classmethod
    def update_customer(
        cls,
        customer_id,
        new_name=None,
        new_phone_number=None
    ):
        """
        update_customer: Updates the information of a customer.
        """
        founded = False
        customers = cls.load_customers()
        for customer in customers:
            if customer["customer_id"] == customer_id:
                founded = True
                if new_name:
                    customer["name"] = new_name
                if new_phone_number:
                    customer["phone_number"] = new_phone_number
                break
        with open(cls.customers_file, 'w', encoding="utf-8") as file:
            json.dump(customers, file, indent=4)
        if not founded:
            print("Customer not found")
        return founded
