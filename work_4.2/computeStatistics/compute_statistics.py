"""
This script utilizes the `datetime`, `sys`, and `time` modules 
to perform operations related to date and time, handle system-related 
functionality, and measure execution time, respectively. 
"""
from datetime import datetime
import sys
import time

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
                        number = float(line)
                        data.append(number)
                    except ValueError:
                        print(f"Warning: Ignoring non-numeric value in the file: {line}")
        return data
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading file: {e}")
        return None

def calculate_mean(data):
    """
    func: Calculates the mean (average) of a list of numeric data.
    """
    return sum(data) / len(data)

def calculate_median(data):
    """
    func: Calculates the median of a list of numeric data.
    """
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    return sorted_data[mid]

def calculate_mode(data):
    """
    func: Calculate the mode of a list of numeric data. 
    """
    if len(set(data)) == len(data):
        return "#N/A"
    return max(set(data), key=data.count)

def calculate_standard_deviation(data):
    """
    func: Calculates the standard deviation of a list of numeric data.
    """
    return (sum((x-(sum(data) / len(data)))**2 for x in data) / (len(data)-1))**0.5

def calculate_variance(data):
    """
    func: Calculate the variance of a list of numeric data.
    """
    return sum((xi - calculate_mean(data)) ** 2 for xi in data) / len(data)

def main():
    """
    Main function for computing statistics on data from a file.
    """
    start_time = time.time()
    if len(sys.argv) != 2:
        print("Usage: python compute_statistics.py fileWithData.txt")
        sys.exit(1)

    file_path = sys.argv[1]

    data = read_file(file_path)

    if data is None:
        sys.exit(1)

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    count = len(data)

    mean = calculate_mean(data)

    median = calculate_median(data)

    mode = calculate_mode(data)

    sd = calculate_standard_deviation(data)

    var = calculate_variance(data)

    end_time = time.time()
    final_time = end_time - start_time

    result_text = "---------------------------------------------------\n"
    result_text += (f"Execution: {formatted_datetime}\n")
    result_text += (f"{file_path}\n")
    result_text += (f"Count: {count}\n")
    result_text += (f"Mean: {mean}\n")
    result_text += (f"Median: {median}\n")
    result_text += (f"Mode: {mode}\n")
    result_text += (f"Standard Deviation: {sd}\n")
    result_text += (f"Variance: {var}\n")
    result_text += (f"Elapsed Time: {final_time} seconds\n")

    with open("StatisticsResults.txt", 'a', encoding='utf-8') as results_file:
        results_file.write(result_text)
    print(result_text)

if __name__ == "__main__":
    main()
    