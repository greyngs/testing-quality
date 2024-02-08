"""
This script utilizes the following modules:
- `datetime` for operations related to date and time.
- `sys` for handling system-related functionality.
- `time` for measuring execution time.
- `json` for encoding and decoding JSON data.
"""
from datetime import datetime
import sys
import time
import json


def read_file(file_path):
    """
    Reads data from a JSON file located at the specified file path.

    Args:
    file_path (str): The path to the JSON file to be read.

    Returns:
    list or None: A list containing the data from the JSON file
    if the file is successfully read and decoded,
    or None if an error occurs during the process.

    Raises:
    FileNotFoundError: If the specified file cannot be found.
    JSONDecodeError: If the JSON decoding process encounters an error.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading files: {e}")
        return None


def main():
    """
    Calculates the total cost of sales from JSON files, handles invalid data,
    and prints/writes results.

    Args:
        None

    Returns:
        None
    """
    start_time = time.time()

    if len(sys.argv) != 3:
        print("Usage: python compute_sales.py "
              "priceCatalogue.json salesRecord.json")
        sys.exit(1)

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    price_catalogue = read_file(sys.argv[1])
    sales_records = read_file(sys.argv[2])

    if not price_catalogue or not sales_records:
        sys.exit(1)

    total_cost = 0

    for sale in sales_records:
        sale_id = sale.get("SALE_ID")
        sale_date = sale.get("SALE_Date")
        product_name = sale.get("Product")
        quantity = sale.get("Quantity")

        if not all((sale_id, sale_date, product_name, quantity)):
            print(f"Invalid sale record: {sale}")
            continue

        product_price = 0
        for product in price_catalogue:
            if product["title"].lower() == product_name.lower():
                product_price = product["price"]
                break

        if not product_price:
            print(f"Product '{product_name}' not found in price catalogue")
            continue

        total_cost += product_price * quantity

    result_text = "--------------------------------------------\n"
    result_text += (f"Execution: {formatted_datetime}\n")
    result_text += (f"Product list file: {sys.argv[1]}\n"
                    f"Sales file: {sys.argv[2]}\n")
    result_text += (f"Total: {total_cost:.2f}\n")
    result_text += (f"Elapsed Time: {time.time() - start_time} seconds\n")

    with open("SalesResults.txt", 'a', encoding='utf-8') as results_file:
        results_file.write(result_text)
    print(result_text)


if __name__ == "__main__":
    main()
