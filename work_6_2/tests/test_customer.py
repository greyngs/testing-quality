"""
This script contains the unit tests for the Customer class.

It utilizes the following modules:
- `unittest` for running the tests.
- `unittest.mock` for mocking standard output.
- `json` for encoding and decoding JSON data.
- `io` for handling input/output operations.
- `Customer` from `booking.customers.customer` for testing the Customer class.
"""
import unittest
import unittest.mock
import json
import io
from booking.customers.customer import Customer

class TestCustomer(unittest.TestCase):
    """
    Class to test the Customer class.
    """

    def setUp(self):
        """
        setUp: Initializes a new Customer object for each test.
        """
        self.customer = Customer("123", "Test Jorge", "57-987-4321")

    def test_customer_initialization(self):
        """
        test_customer_initialization: Tests the initialization of a Customer object.
        """
        self.assertEqual(self.customer.customer_id, "123")
        self.assertEqual(self.customer.name, 'Test Jorge')
        self.assertEqual(self.customer.phone_number, "57-987-4321")

    def test_to_dict(self):
        """
        test_to_dict: Tests the to_dict method of a Customer object.
        """
        expected_dict = {
            "customer_id": self.customer.customer_id,
            "name": self.customer.name,
            "phone_number": self.customer.phone_number
        }
        self.assertEqual(self.customer.to_dict(), expected_dict)

    def test_load_customers(self):
        """
        test_load_customers: Tests the load_customers method of the Customer class.
        """
        customers = Customer.load_customers()
        self.assertIsInstance(customers, list)

    def test_save_to_json(self):
        """
        test_save_to_json: Tests the save_to_json method of a Customer object.
        """
        self.customer.save_to_json()
        with open(Customer.customers_file, 'r', encoding='utf-8') as file:
            customers = json.load(file)
        self.assertIn(self.customer.to_dict(), customers)
        Customer.delete_customer(self.customer.customer_id)

    def test_create_customer_affirmative(self):
        """
        test_create_customer_affirmative: Tests the create_customer method of the Customer class.
        """
        save_customer_id = "123"
        save_name = "Jauanita"
        save_phone_number = "555-987-6543"
        save_customer = Customer.create_customer(save_customer_id, save_name, save_phone_number)
        customers = Customer.load_customers()
        self.assertIn(save_customer.to_dict(), customers)
        Customer.delete_customer(save_customer.customer_id)

    def test_create_customer_invalid_customer_id(self):
        """
        test_create_customer_invalid_customer_id: Tests the create_customer
        method with an invalid customer_id.
        """
        invalid_customer_id = 123
        invalid_name = "Juanita"
        invalid_phone_number = "555-987-6543"
        invalid_customer = Customer.create_customer(
            invalid_customer_id,
            invalid_name,
            invalid_phone_number
        )
        self.assertIsNone(invalid_customer)

    def test_create_customer_invalid_customer_name(self):
        """
        test_create_customer_invalid_customer_name: Tests the create_customer
        method with an invalid name.
        """
        invalid_customer_id = "123"
        invalid_name = 123
        invalid_phone_number = "555-987-6543"
        invalid_customer = Customer.create_customer(
            invalid_customer_id,
            invalid_name,
            invalid_phone_number
        )
        self.assertIsNone(invalid_customer)

    def test_create_customer_invalid_customer_phone_number(self):
        """
        test_create_customer_invalid_customer_phone_number: Tests the create_customer
        method with an invalid phone_number.
        """
        invalid_customer_id = "123"
        invalid_name = "Juanita"
        invalid_phone_number = 123
        invalid_customer = Customer.create_customer(
            invalid_customer_id,
            invalid_name,
            invalid_phone_number
        )
        self.assertIsNone(invalid_customer)

    def test_delete_customer_affirmative(self):
        """
        test_delete_customer_affirmative: Tests the delete_customer method of the Customer class.
        """
        self.customer.save_to_json()
        self.assertTrue(Customer.delete_customer(self.customer.customer_id))

    def test_delete_customer_negative(self):
        """
        test_delete_customer_negative: Tests the delete_customer method with an invalid customer_id.
        """
        self.customer.save_to_json()
        self.assertFalse(Customer.delete_customer("Bad_Id"))
        Customer.delete_customer(self.customer.customer_id)

    def test_display_non_existing_customer(self):
        """
        test_display_non_existing_customer: Tests the display_customer method with a 
        non-existing customer_id.
        """
        with unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            Customer.display_customer("999")
            output = fake_stdout.getvalue().strip()
            self.assertEqual(output, "Customer not found")

    def test_update_customer(self):
        """
        test_update_customer: Tests the update_customer method of the Customer class.
        """
        self.customer.save_to_json()
        new_name = "Jane Doe"
        new_phone_number = "555-987-6543"
        self.assertTrue(Customer.update_customer(self.customer.customer_id,
                                                 new_name,
                                                 new_phone_number
                                                ))
        customers = Customer.load_customers()
        updated_customer = next(
            (c for c in customers if c["customer_id"] == self.customer.customer_id),
            None
        )
        self.assertIsNotNone(updated_customer)
        self.assertEqual(updated_customer["name"], new_name)
        self.assertEqual(updated_customer["phone_number"], new_phone_number)

if __name__ == '__main__':
    unittest.main()
