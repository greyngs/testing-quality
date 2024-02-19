"""
This script utilizes the `datetime`, `sys`, and `time` modules 
to perform operations related to date and time, handle system-related 
functionality, and measure execution time, respectively. 
"""
from datetime import datetime
import sys
import time

conversion_table = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4',
                    5: '5', 6: '6', 7: '7',
                    8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C',
                    13: 'D', 14: 'E', 15: 'F'}

def read_file(file_path):
    """
    func: Reads numeric data from a file and returns a list of floats.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = []
            for line in file:
                line = line.strip()
                if line:
                    try:
                        number = int(line)
                        data.append(number)
                    except ValueError:
                        print(f"Warning: Ignoring non-numeric value in the file: {line}")
        return data
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading file: {e}")
        return None

def dec2bin(number):
    """
    Converts a decimal number to its binary representation.
    """
    if number == 0:
        return '0'

    ans = ""
    is_negative = False

    if number < 0:
        is_negative = True
        number = abs(number)

    while number:
        ans += str(number & 1)
        number = number >> 1

    ans = ans[::-1]

    if is_negative:
        ans = ans.rjust(10, '0')
        ans = ''.join('1' if bit == '0' else '0' for bit in ans)
        ans = bin(int(ans, 2) + 1)[2:]

    return ans

def dec2hex(decimal):
    """
    Converts a decimal number to its hexadecimal representation.
    """
    if decimal == 0:
        return '0'

    is_negative = False

    if decimal < 0:
        is_negative = True
        decimal = abs(decimal)

    hexadecimal = ''

    while decimal > 0:
        remainder = decimal % 16
        hexadecimal = conversion_table[remainder] + hexadecimal
        decimal = decimal // 16

    if is_negative:
        hexadecimal = hexadecimal.rjust(8, '0')
        hexadecimal = ''.join(conversion_table[15 - int(bit, 16)] for bit in hexadecimal)
        hexadecimal = hex(int(hexadecimal, 16) + 1)[2:].upper()

    return hexadecimal

def main():
    """
    Main function for computing statistics on data from a file.
    """
    start_time = time.time()
    if len(sys.argv) != 2:
        print("Usage: python convert_numbers.py fileWithData.txt")
        sys.exit(1)

    file_path = sys.argv[1]

    data = read_file(file_path)

    if data is None:
        sys.exit(1)

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    count = len(data)

    end_time = time.time()
    final_time = end_time - start_time

    result_text = "---------------------------------------------------\n"
    result_text += (f"Execution: {formatted_datetime}\n")
    result_text += (f"{file_path}\n")
    result_text += (f"Count: {count}\n")
    result_text += ("NUMBER\tDEC\tBIN\tHEX\n")
    for index, value in enumerate(data):
        result_text += f"{index + 1}\t{value}\t{dec2bin(value)}\t{dec2hex(value)}\n"
    result_text += (f"Elapsed Time: {final_time} seconds\n")

    with open("ConvertionResults.txt", 'a', encoding='utf-8') as results_file:
        results_file.write(result_text)
    print(result_text)

if __name__ == "__main__":
    main()
 