"""
This script utilizes the `datetime`, `sys`, and `time` modules 
to perform operations related to date and time, handle system-related 
functionality, and measure execution time, respectively. 
"""
from datetime import datetime
import sys
import time
import os

def main():
    """
    Main function for computing statistics on data from a file.
    """
    start_time = time.time()
    if len(sys.argv) != 2:
        print("Usage: python word_count.py fileWithData.txt")
        sys.exit(1)

    occurrences = {}
    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as file:
            for line in file:
                words = line.split()
                for word in words:
                    occurrences[word] = occurrences.get(word, 0) + 1
        sorted_occurrences = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading file: {e}")

    if sorted_occurrences is None:
        sys.exit(1)

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    end_time = time.time()
    file_name, _ = os.path.splitext(sys.argv[1])

    result_text = "---------------------------------------------------\n"
    result_text += (f"Execution: {formatted_datetime}\n")
    result_text += (f"{sys.argv[1]}\n")
    result_text += (f"Count: {len(sorted_occurrences)}\n")
    result_text += ("Row labels\tCount\n")
    for word, frequency in sorted_occurrences:
        result_text += (f"{word}\t{frequency}\n")
    result_text += (f"Elapsed Time: {end_time - start_time} seconds\n")

    with open(f"{file_name}_wordCountResults.txt", 'a', encoding='utf-8') as results_file:
        results_file.write(result_text)
    print(result_text)

if __name__ == "__main__":
    main()
 